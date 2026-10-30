"""Worked example for CADFEM-Bench task A-GEOPINO-PLATE-1: a holed steel plate, fixed at one end, loaded at the other in
two separate linear static load cases (compression along -y, lateral shear along +x). Written by hand to show every
stage of a CAD -> mesh -> FEM -> results workflow; each stage logs what it did and the check that guards it.

Runs offline: reads CADFEM_INPUT_DIR/part.step, writes results.json, part.step, mesh.msh, fields.npz, solver.log,
refinement.json and environment.json to CADFEM_OUTPUT_DIR.
"""
import json, os, platform, shutil, sys, time
from pathlib import Path

import gmsh
import numpy as np
import scipy
import skfem
from scipy.sparse.linalg import splu
from skfem import MeshTet, Basis, FacetBasis, ElementVector, ElementTetP2, Functional, LinearForm, asm, condense
from skfem.models.elasticity import linear_elasticity, lame_parameters

IN = Path(os.environ.get("CADFEM_INPUT_DIR", "."))
OUT = Path(os.environ.get("CADFEM_OUTPUT_DIR", "out"))
OUT.mkdir(parents=True, exist_ok=True)
T0 = time.time()
LOG = open(OUT / "solver.log", "w")


def log(*parts):
    line = f"[{time.time() - T0:7.2f} s] " + " ".join(str(p) for p in parts)
    print(line, flush=True)
    LOG.write(line + "\n"); LOG.flush()


# Data from the prompt (units: mm, N, MPa)
E, NU, FORCE = 200000.0, 0.3, 1000.0
LX, LY, TZ = 176.914, 148.475, 10.0
CASES = {"max_displacement_compression_mm": np.array([0.0, -1.0, 0.0]),   # load case 1: towards the fixed end
         "max_displacement_lateral_mm": np.array([1.0, 0.0, 0.0])}        # load case 2: in-plane shear of the free end
SIZES_MM = [10.0, 7.0, 5.0]                                                  # three meshes for the convergence record


def geometry():
    """Stage 2: open the CAD, check it is the part the prompt describes, and find the two end faces."""
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("Geometry.OCCBoundsUseStl", 1)        # exact box from the surface, not the control points
    gmsh.model.add("plate")
    gmsh.model.occ.importShapes(str(IN / "part.step"))
    gmsh.model.occ.synchronize()
    vols = gmsh.model.getEntities(3)
    if len(vols) != 1:
        raise RuntimeError(f"expected one solid, found {len(vols)}")
    box = gmsh.model.getBoundingBox(3, vols[0][1])
    dims = (box[3] - box[0], box[4] - box[1], box[5] - box[2])
    log("CAD:", [len(gmsh.model.getEntities(d)) for d in range(4)], "points/curves/surfaces/volumes; size",
        " x ".join(f"{d:.3f}" for d in dims), "mm; volume", f"{gmsh.model.occ.getMass(3, vols[0][1]):.1f} mm3")
    if any(abs(a - b) > 0.01 for a, b in zip(dims, (LX, LY, TZ))):
        raise RuntimeError(f"CAD size {dims} does not match the prompt {(LX, LY, TZ)}")
    fixed = loaded = None
    for _, s in gmsh.model.getEntities(2):
        c, a = gmsh.model.occ.getCenterOfMass(2, s), gmsh.model.occ.getMass(2, s)
        if gmsh.model.getType(2, s) == "Plane" and abs(a - LX * TZ) < 0.5:
            if abs(c[1] - box[1]) < 1e-3: fixed = s
            if abs(c[1] - box[4]) < 1e-3: loaded = s
    if fixed is None or loaded is None:
        raise RuntimeError("could not find the two end faces")
    log(f"faces: fixed = surface {fixed} (y = {box[1]:.4f}), loaded = surface {loaded} (y = {box[4]:.4f}), area {LX * TZ:.2f} mm2 each")
    return box


def mesh(h):
    """Stage 3: linear tetrahedra from Gmsh; quadratic (P2) fields are added on straight edges by scikit-fem."""
    gmsh.model.mesh.clear()
    gmsh.option.setNumber("Mesh.MeshSizeMin", h)
    gmsh.option.setNumber("Mesh.MeshSizeMax", h)
    gmsh.option.setNumber("Mesh.Optimize", 1)
    gmsh.model.mesh.generate(3)
    tags, xyz, _ = gmsh.model.mesh.getNodes()
    p = xyz.reshape(-1, 3)
    index = np.full(int(tags.max()) + 1, -1); index[tags.astype(int)] = np.arange(len(tags))
    etypes, _, enodes = gmsh.model.mesh.getElements(3)
    t = index[enodes[list(etypes).index(4)].astype(int)].reshape(-1, 4)
    used = np.unique(t); remap = np.full(len(p), -1); remap[used] = np.arange(len(used))
    p, t = p[used], remap[t]
    vol = np.einsum("ij,ij->i", np.cross(p[t[:, 1]] - p[t[:, 0]], p[t[:, 2]] - p[t[:, 0]]), p[t[:, 3]] - p[t[:, 0]]) / 6
    t[vol < 0] = t[vol < 0][:, [0, 2, 1, 3]]                    # orient every element positively
    vol = np.abs(vol)
    if vol.min() <= 1e-9 * vol.mean():
        raise RuntimeError("degenerate element in the mesh")
    return p, t, float(vol.sum())


def solve_level(p, t, box):
    """Stage 4: assemble K, apply the support and the end tractions, solve K u = f for both load cases."""
    m = MeshTet(p.T, t.T)
    e = ElementVector(ElementTetP2())
    ib = Basis(m, e, intorder=4)
    lam, mu = lame_parameters(E, NU)
    K = asm(linear_elasticity(lam, mu), ib)
    fixed = ib.get_dofs(lambda x: np.abs(x[1] - box[1]) < 1e-6).all()
    fb = FacetBasis(m, e, facets=m.facets_satisfying(lambda x: np.abs(x[1] - box[4]) < 1e-6), intorder=4)
    area = Functional(lambda w: 1.0 + 0.0 * w.x[0]).assemble(fb)
    log(f"  K: {K.shape[0]} unknowns, {K.nnz} nonzeros; fixed dofs {len(fixed)}; loaded area {area:.3f} mm2")
    I = ib.complement_dofs(fixed)
    lu = splu(K[I][:, I].tocsc())
    out, fields = {}, {}
    for key, d in CASES.items():
        tv = FORCE / area * d                                       # uniform traction: total force / face area

        @LinearForm
        def traction(v, w):
            return tv[0] * v[0] + tv[1] * v[1] + tv[2] * v[2]
        f = asm(traction, fb)
        u = np.zeros(K.shape[0]); u[I] = lu.solve(f[I])
        r = K @ u - f                                               # reactions live on the fixed dofs
        comp = [np.concatenate([ib.nodal_dofs[k], ib.edge_dofs[k]]) for k in range(3)]
        applied = np.array([f[c].sum() for c in comp])
        reaction = np.array([r[np.intersect1d(c, fixed)].sum() for c in comp])
        resid = np.linalg.norm(r[I]) / max(np.linalg.norm(f), 1e-30)
        un, ue = u[ib.nodal_dofs].T, u[ib.edge_dofs].T
        umax = float(max(np.linalg.norm(un, axis=1).max(), np.linalg.norm(ue, axis=1).max()))
        log(f"  {key}: max |u| = {umax:.6e} mm; applied {np.round(applied, 6)} N; reaction {np.round(reaction, 6)} N; "
            f"balance error {np.linalg.norm(applied + reaction) / FORCE:.1e}; residual {resid:.1e}")
        if np.linalg.norm(applied + reaction) > 1e-6 * FORCE or abs(np.linalg.norm(applied) - FORCE) > 1e-6 * FORCE:
            raise RuntimeError("force balance check failed")
        out[key] = umax
        fields[key] = un
    return out, fields, dict(unknowns=int(K.shape[0]), vertices=int(p.shape[0]), elements=int(t.shape[0]))


def main():
    log("A-GEOPINO-PLATE-1 worked example: scikit-fem", skfem.__version__, "(P2 tetrahedra), Gmsh", gmsh.__version__, ", SciPy SuperLU")
    box = geometry()
    shutil.copy(IN / "part.step", OUT / "part.step")               # the geometry analysed is the supplied CAD, unchanged
    levels = []
    for h in SIZES_MM:
        p, t, vol = mesh(h)
        log(f"mesh h = {h} mm: {len(t)} tetrahedra, {len(p)} vertices, mesh volume {vol:.1f} mm3")
        out, fields, size = solve_level(p, t, box)
        levels.append(dict(h_mm=h, **size, outputs=out))
    gmsh.write(str(OUT / "mesh.msh"))                               # the finest mesh, behind the reported numbers
    gmsh.finalize()
    for a, b in zip(levels, levels[1:]):
        b["change_from_previous_percent"] = {k: 100 * abs(b["outputs"][k] / a["outputs"][k] - 1) for k in CASES}
    last = levels[-1]["change_from_previous_percent"]
    log("convergence (finest vs previous mesh):", {k: f"{v:.3f} %" for k, v in last.items()})
    if max(last.values()) > 1.0:
        raise RuntimeError("not converged to 1 %")
    (OUT / "refinement.json").write_text(json.dumps(dict(levels=levels, element="P2 tetrahedra (10 nodes, straight edges)",
                                                          criterion="each output changes by less than 1 % between the two finest meshes"), indent=2))
    np.savez_compressed(OUT / "fields.npz", points=p, tetra=t, **{f"displacement_{k}": v for k, v in fields.items()},
                        units=np.array("mm"))
    (OUT / "environment.json").write_text(json.dumps(dict(python=sys.version.split()[0], platform=platform.platform(),
                                                          gmsh=gmsh.__version__, scikit_fem=skfem.__version__,
                                                          numpy=np.__version__, scipy=scipy.__version__), indent=2))
    (OUT / "results.json").write_text(json.dumps({"outputs": levels[-1]["outputs"]}, indent=2))
    log("results.json:", levels[-1]["outputs"])


if __name__ == "__main__":
    main()
