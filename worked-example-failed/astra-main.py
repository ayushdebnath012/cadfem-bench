import os
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["CCX_NPROC_RESULTS"] = "2"
os.environ["CCX_NPROC_EQUATION_SOLVER"] = "2"

import json
import math
import re
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np


START = time.monotonic()
INPUT = Path(os.environ.get("CADFEM_INPUT_DIR", ".")).resolve()
OUTPUT = Path(os.environ.get("CADFEM_OUTPUT_DIR", ".")).resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)
LOG = OUTPUT / "solver.log"


def log(message):
    with LOG.open("a") as f:
        f.write(str(message) + "\n")
    print(message, flush=True)


def validate_geometry():
    import gmsh

    data = json.loads((INPUT / "faces.json").read_text())
    descriptors = data["face_descriptors"] if isinstance(data, dict) else data
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("supplied_analysis_geometry")
        gmsh.model.occ.importShapes(str(INPUT / "analysis.step"))
        gmsh.model.occ.synchronize()
        solids = gmsh.model.getEntities(3)
        surfaces = gmsh.model.getEntities(2)
        if len(solids) != 1 or len(surfaces) != 6:
            raise RuntimeError("Expected one six-faced rectangular solid.")
        matched = {}
        unused = set(tag for _, tag in surfaces)
        for d in descriptors:
            c = np.array(d["centroid_mm"], dtype=float)
            tag = min(
                unused,
                key=lambda t: np.linalg.norm(
                    np.array(gmsh.model.occ.getCenterOfMass(2, t)) - c
                ),
            )
            actual_c = np.array(gmsh.model.occ.getCenterOfMass(2, tag))
            area = gmsh.model.occ.getMass(2, tag)
            kind = gmsh.model.getType(2, tag)
            if np.linalg.norm(actual_c - c) > 1e-4:
                raise RuntimeError("CAD face centroid does not match faces.json.")
            if abs(area - d["area_mm2"]) > max(1e-4, area * 1e-6):
                raise RuntimeError("CAD face area does not match faces.json.")
            if kind.lower() != "plane":
                raise RuntimeError("Structured solid mesh requires planar CAD faces.")
            bbox = np.array(gmsh.model.getBoundingBox(2, tag))
            if "bbox_mm" in d:
                if np.max(np.abs(bbox - np.array(d["bbox_mm"]))) > 1e-3:
                    raise RuntimeError("CAD face bounds do not match faces.json.")
            unused.remove(tag)
            matched[int(d["face_index"])] = actual_c
            log(f"CAD face {d['face_index']} -> surface {tag}: "
                f"type={kind}, area={area:.12g}, centroid={actual_c.tolist()}")
        if set(matched) != set(range(1, 7)):
            raise RuntimeError("Missing required face descriptors.")
        bounds = (
            matched[1][0], matched[2][0],
            matched[3][1], matched[4][1],
            matched[5][2], matched[6][2],
        )
        xmin, xmax, ymin, ymax, zmin, zmax = bounds
        lengths = np.array([xmax - xmin, ymax - ymin, zmax - zmin])
        if np.any(lengths <= 0):
            raise RuntimeError("Invalid geometry extents.")
        volume = gmsh.model.occ.getMass(3, solids[0][1])
        if abs(volume - np.prod(lengths)) > volume * 1e-6:
            raise RuntimeError("CAD solid is not the verified rectangular prism.")
        expected_areas = {
            1: lengths[1] * lengths[2], 2: lengths[1] * lengths[2],
            3: lengths[0] * lengths[2], 4: lengths[0] * lengths[2],
            5: lengths[0] * lengths[1], 6: lengths[0] * lengths[1],
        }
        for d in descriptors:
            if not math.isclose(d["area_mm2"],
                                expected_areas[int(d["face_index"])],
                                rel_tol=1e-6, abs_tol=1e-4):
                raise RuntimeError("Rectangular-prism area validation failed.")
        log(f"Verified STEP volume={volume:.12g} mm^3; bounds={bounds}")
        return bounds
    finally:
        gmsh.finalize()


OFFSETS = [
    (0, 0, 0), (2, 0, 0), (2, 2, 0), (0, 2, 0),
    (0, 0, 2), (2, 0, 2), (2, 2, 2), (0, 2, 2),
    (1, 0, 0), (2, 1, 0), (1, 2, 0), (0, 1, 0),
    (1, 0, 2), (2, 1, 2), (1, 2, 2), (0, 1, 2),
    (0, 0, 1), (2, 0, 1), (2, 2, 1), (0, 2, 1),
]


def write_set(f, name, values):
    f.write(f"*NSET,NSET={name}\n")
    for k in range(0, len(values), 16):
        f.write(",".join(str(v) for v in values[k:k + 16]) + "\n")


def create_model(bounds, nx, ny, nz, name):
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    nodes = {}
    elements = []
    forces = {}
    face_area = (ymax - ymin) * (zmax - zmin) / (ny * nz)
    traction = -282.772

    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                conn = []
                for a, b, c in OFFSETS:
                    key = (2 * i + a, 2 * j + b, 2 * k + c)
                    if key not in nodes:
                        nodes[key] = len(nodes) + 1
                    conn.append(nodes[key])
                elements.append(conn)
                if i == nx - 1:
                    # Exact consistent nodal integral of uniform traction on
                    # an eight-node serendipity face: corners -A/12, edges A/3.
                    for local in (1, 2, 6, 5):
                        node = conn[local]
                        forces[node] = forces.get(node, 0.0) - traction * face_area / 12
                    for local in (9, 18, 13, 17):
                        node = conn[local]
                        forces[node] = forces.get(node, 0.0) + traction * face_area / 3

    fixed = sorted(n for (i, j, k), n in nodes.items() if i == 0)
    supported_z = sorted(
        n for (i, j, k), n in nodes.items()
        if i != 0 and (i == 2 * nx or j == 0 or j == 2 * ny)
    )
    total_force = sum(forces.values())
    expected_force = traction * (ymax - ymin) * (zmax - zmin)
    if not math.isclose(total_force, expected_force, rel_tol=1e-11):
        raise RuntimeError("Consistent traction integration failed.")
    model = OUTPUT / (name + "_model.inc")
    with model.open("w") as f:
        f.write("*NODE,NSET=NALL\n")
        for (i, j, k), n in nodes.items():
            xyz = (
                xmin + (xmax - xmin) * i / (2 * nx),
                ymin + (ymax - ymin) * j / (2 * ny),
                zmin + (zmax - zmin) * k / (2 * nz),
            )
            f.write(f"{n},{xyz[0]:.14g},{xyz[1]:.14g},{xyz[2]:.14g}\n")
        f.write("*ELEMENT,TYPE=C3D20R,ELSET=EALL\n")
        for e, conn in enumerate(elements, 1):
            f.write(",".join(map(str, [e] + conn[:15])) + ",\n")
            f.write(",".join(map(str, conn[15:])) + "\n")
        write_set(f, "FIXED", fixed)
        write_set(f, "ZSUPPORT", supported_z)
        f.write("*MATERIAL,NAME=ALUMINIUM\n*ELASTIC\n70000.,0.33\n")
        f.write("*SOLID SECTION,ELSET=EALL,MATERIAL=ALUMINIUM\n")
        f.write("*BOUNDARY\nFIXED,1,3\nZSUPPORT,3,3\n")
    loadfile = OUTPUT / (name + "_load.inc")
    with loadfile.open("w") as f:
        f.write("*CLOAD\n")
        for n, force in sorted(forces.items()):
            f.write(f"{n},1,{force:.15g}\n")
    log(f"{name}: C3D20R mesh {nx}x{ny}x{nz}, "
        f"{len(elements)} elements, {len(nodes)} nodes; "
        f"integrated reference Fx={total_force:.12g} N")
    return model.name, loadfile.name


def write_job(name, model, loads, buckling):
    with (OUTPUT / (name + ".inp")).open("w") as f:
        f.write("*HEADING\n")
        f.write("Verified STEP plate: solid elastic reference-load buckling\n")
        f.write(f"*INCLUDE,INPUT={model}\n")
        f.write("*STEP\n")
        if buckling:
            f.write("*BUCKLE\n8,0.0001\n")
        else:
            f.write("*STATIC\n1.,1.\n")
        f.write(f"*INCLUDE,INPUT={loads}\n")
        f.write("*NODE FILE,GLOBAL=YES\nU,RF\n")
        f.write("*EL FILE\nS,E\n")
        if not buckling:
            f.write("*NODE PRINT,NSET=FIXED,TOTALS=YES\nRF\n")
            f.write("*EL PRINT,ELSET=EALL\nS,E\n")
        f.write("*END STEP\n")


def run_ccx(executable, name, timeout):
    logfile = OUTPUT / (name + ".stdout.log")
    log(f"Running {name}; timeout={timeout:.0f} s")
    before = time.monotonic()
    with logfile.open("w") as f:
        process = subprocess.Popen(
            [executable, "-i", name], cwd=str(OUTPUT),
            stdout=f, stderr=subprocess.STDOUT, env=os.environ.copy()
        )
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            with LOG.open("a") as master:
                master.write(logfile.read_text(errors="replace"))
            raise TimeoutError(f"CalculiX timeout in {name}")
    text = logfile.read_text(errors="replace")
    with LOG.open("a") as master:
        master.write(f"\n--- {name}: full CalculiX console output ---\n")
        master.write(text)
        master.write("\n--- end console output ---\n")
    duration = time.monotonic() - before
    if code != 0 or re.search(r"\*ERROR", text, flags=re.I):
        raise RuntimeError(f"CalculiX failed in {name}; see retained log.")
    log(f"{name} completed in {duration:.2f} s")
    return duration


def read_factors(name):
    path = OUTPUT / (name + ".dat")
    text = path.read_text(errors="replace")
    rows = []
    active = False
    number = r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[EeDd][+-]?\d+)?"
    for line in text.splitlines():
        compressed = re.sub(r"\s+", "", line).upper()
        if "BUCKLINGFACTOR" in compressed:
            active = True
            continue
        if active:
            match = re.match(r"^\s*(\d+)\s+(" + number + r")\s*$", line)
            if match:
                rows.append((int(match.group(1)),
                             float(match.group(2).replace("D", "E").replace("d", "e"))))
    if not rows:
        raise RuntimeError(f"No buckling factors found in {path}")
    positive = [value for _, value in rows if math.isfinite(value) and value > 0]
    if not positive:
        raise RuntimeError("No positive elastic buckling factors were computed.")
    log(f"{name}: computed buckling factors {rows}")
    return min(positive), rows


def main():
    LOG.write_text(
        "Linear elastic solid buckling analysis; units N, mm, MPa.\n"
        "Material E=70000 MPa, nu=0.33; no self-weight.\n"
        "Actual STEP geometry is validated before generating a conforming "
        "structured quadratic solid mesh.\n"
        "CalculiX *BUCKLE on the initially unloaded body computes the linear "
        "reference-load stress state and solves the elastic buckling problem. "
        "The same load is independently solved with *STATIC on the selected mesh "
        "to retain reference displacements, reactions, strains and stresses. "
        "No preloading is added to the buckling load set.\n"
    )
    resultfile = OUTPUT / "results.json"
    if resultfile.exists():
        resultfile.unlink()
    executable = shutil.which("ccx")
    if not executable:
        raise RuntimeError("CalculiX executable ccx not found.")
    bounds = validate_geometry()
    history = []
    selected = None
    previous_duration = 0.0
    meshes = [(32, 16, 2), (48, 24, 2), (64, 32, 3)]

    for index, mesh in enumerate(meshes):
        remaining = 565 - (time.monotonic() - START)
        if index >= 2:
            # Preserve enough time for an independent static field solution.
            estimated_next = max(45.0, previous_duration * 3.0)
            if remaining < estimated_next + max(70.0, previous_duration * 1.5):
                log("Third refinement omitted to reserve time for static fields; "
                    "no convergence claim is made for an uncomputed mesh.")
                break
        name = f"mesh_{mesh[0]}_{mesh[1]}_{mesh[2]}"
        model, loads = create_model(bounds, *mesh, name)
        job = name + "_buckling"
        write_job(job, model, loads, True)
        timeout = max(20.0, min(240.0, remaining - 65.0))
        try:
            previous_duration = run_ccx(executable, job, timeout)
            factor, factors = read_factors(job)
        except (RuntimeError, TimeoutError) as error:
            if selected is None:
                raise
            log(f"Refinement unsuccessful: {error}; retaining last successful mesh.")
            break
        record = {
            "mesh": list(mesh),
            "lambda1": factor,
            "computed_factors": factors,
            "solver_seconds": previous_duration,
        }
        if history:
            change = abs(factor - history[-1]["lambda1"]) / abs(factor)
            record["relative_change_from_previous"] = change
            log(f"Observed refinement change in lambda1: {100 * change:.6g}%")
        history.append(record)
        selected = (name, model, loads, factor)
        (OUTPUT / "refinement.json").write_text(json.dumps(history, indent=2))

    if selected is None:
        raise RuntimeError("No successful eigenvalue analysis.")
    name, model, loads, factor = selected
    static_job = name + "_reference_static"
    write_job(static_job, model, loads, False)
    remaining = 585 - (time.monotonic() - START)
    if remaining < 10:
        raise RuntimeError("Insufficient time to retain reference static fields.")
    run_ccx(executable, static_job, remaining)
    if not (OUTPUT / (static_job + ".frd")).exists():
        raise RuntimeError("Reference static field file was not generated.")
    log(f"Selected finest successful mesh: {name}; lambda1={factor:.12g}")
    log("Reference stresses/strains are retained in static .dat and .frd; "
        "buckling mode displacements in buckling .frd. "
        "Refinement values are measured solver results, not extrapolated.")
    resultfile.write_text(json.dumps({"outputs": {"lambda1": float(factor)}}, indent=2))
    log(f"Total elapsed time: {time.monotonic() - START:.2f} s")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        with LOG.open("a") as f:
            f.write(traceback.format_exc())
        raise
