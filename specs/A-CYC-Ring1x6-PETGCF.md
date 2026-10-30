# A-CYC-Ring1x6-PETGCF

**The gearbox's spacer ring 1x6 (printed in PETG-CF), held where it mounts and loaded as in use. How far does it bend at most?**

Family: 3D-printed gearbox parts · Set: Main · Physics: Stress and bending · Track A: the CAD file is given

## Overview

Parts from an open-source, 3D-printable 15:1 cycloidal gearbox, mostly printed in carbon-fibre-filled PETG. Each part is held where it mounts and loaded the way the gearbox loads it.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (part.step, faces.json).
2. Load part.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them), then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_displacement_mm, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from CalculiX (the gearbox publisher's own model), checked by our mesh study; check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `part.step` | 3D CAD file |
| `faces.json` | Face list |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "max_displacement_mm": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `max_displacement_mm` | mm | maximum nodal displacement magnitude in the part |

Files to return:

| File | Must contain |
|---|---|
| `results.json` | the final numbers: {"outputs": {key: number}}, exactly the keys listed, plain JSON numbers |
| `main.py` | the whole program; runs end to end with no human help, reading CADFEM_INPUT_DIR and writing CADFEM_OUTPUT_DIR |
| `part.step` | the geometry actually analysed (for build-from-description tasks: the model's own CAD, checked against our hidden shape) |
| `mesh.msh` | the final mesh behind the reported numbers (Gmsh format) |
| `fields.npz` | the nodal results on that mesh (for example displacement, stress or temperature arrays) |
| `solver.log` | the FEM solver's own output, kept unedited |
| `refinement.json` | each reported value at three or more mesh sizes; the last change should be under 1 % |
| `environment.json` | the software and versions used |

## Evaluation

| Check | Rule |
|---|---|
| `max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: max_displacement_mm | Biggest movement anywhere in the part is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_displacement_mm. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by CalculiX (the gearbox publisher's own model), checked by our mesh study; source: [3D-printable cycloidal drive FEA (jagathsrujan/3d-printable-cycloidal-drive)](https://github.com/jagathsrujan/3d-printable-cycloidal-drive).

## Exact prompt

```text
Component analysis: the spacer ring 1x6 of an open-source, 3D-printable 15:1 cycloidal gearbox. part.step holds the single solid in millimetres (6 faces, volume 27 mm^3). faces.json lists every face with its index, type, area, centroid and normal/axis; use the geometry, not a CAD system's own face numbering.

Material: PETG-CF, linear isotropic elastic, E = 3000 MPa, Poisson ratio 0.36.
Analysis: linear static, small displacements, no gravity, no contact.
Supports: all three displacement components are zero on face 4: plane, area 27.14 mm^2, centroid (98.025, 19.468, 35.374) mm, outward normal (-1.0, -0.0, -0.0).
Load: total force (29.990, 0.000, 0.000) N applied as a uniform surface traction (constant force per unit area) over the loaded face(s): face 3 carries (29.990, 0.000, 0.000) N.
For reference, the source solved this with second-order tetrahedra (Netgen, maximum element size 2 mm).

Outputs:
- max_displacement_mm [mm]: maximum nodal displacement magnitude in the part

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
