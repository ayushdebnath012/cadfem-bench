# A-FCVM-Plate_girder_EC3

**A welded steel plate girder of the kind used in bridges, built from 104 plates. By what factor can the load grow before it buckles?**

Family: Steel structures that buckle (fcVM) · Set: Main · Physics: Buckling · Track A: the CAD file is given

## Overview

Steel examples from the FreeCAD verification workbench, from a single bar to a 30 m welded bridge girder.

Analysis: linear buckling: a static solve under the given load, then the eigenvalue problem K + λ·K_G = 0 for the buckling factors.

## Flow

1. Read the prompt and the input files (analysis.step, faces.json).
2. Load analysis.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them), then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear buckling: a static solve under the given load, then the eigenvalue problem K + λ·K_G = 0 for the buckling factors. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into lambda1, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from the fcVM FreeCAD workbench solver; check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `analysis.step` | 3D CAD file |
| `faces.json` | Face list |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "lambda1": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `lambda1` | - | first (smallest positive) elastic buckling load factor of the reference load set (the factor on the whole given load at which the part first buckles: 0.5 means it buckles at half the load, 2 at twice the load) |

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
| `lambda1` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: lambda1 | Buckling factor: how many times the given load makes it buckle is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: lambda1. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by the fcVM FreeCAD workbench solver; source: [fcVM workbench examples (Harry van Langen, HarryvL/fcVM-workbench)](https://github.com/HarryvL/fcVM-workbench).

## Exact prompt

```text
Linear (eigenvalue) buckling analysis of a steel structure from the fcVM workbench examples (Plate_girder_EC3). analysis.step holds the analysis geometry in millimetres (104 solid region(s) that share their interfaces and act as one continuous body, volume 3335612900 mm^3). faces.json describes every face (index, type, area, centroid, normal/axis).
Material: linear isotropic elastic, E = 210000 MPa, Poisson ratio 0.3.
Supports: (1) all displacement components = 0 along the edge from (50.0, 87.5, 2100.0) to (50.0, 367.5, 2100.0) mm (edge 459 of analysis.step). (2) all displacement components = 0 along the edge from (50.0, 367.5, 2100.0) to (50.0, 382.5, 2100.0) mm (edge 463 of analysis.step). (3) all displacement components = 0 along the edge from (50.0, 382.5, 2100.0) to (50.0, 662.5, 2100.0) mm (edge 464 of analysis.step). (4) displacement u_y, u_z = 0 along the edge from (29950.0, 87.5, 2100.0) to (29950.0, 367.5, 2100.0) mm (edge 517 of analysis.step). (5) displacement u_y, u_z = 0 along the edge from (29950.0, 367.5, 2100.0) to (29950.0, 382.5, 2100.0) mm (edge 528 of analysis.step). (6) displacement u_y, u_z = 0 along the edge from (29950.0, 382.5, 2100.0) to (29950.0, 662.5, 2100.0) mm (edge 529 of analysis.step).
Reference load set (load factor 1): (1) uniform traction (-0.0, 0.0, -166.15942) MPa on face 332: plane, area 6720.00 mm^2, centroid (29938.0, 227.5, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (2) uniform traction (-0.0, 0.0, -166.15942) MPa on face 334: plane, area 360.00 mm^2, centroid (29938.0, 375.0, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (3) uniform traction (-0.0, 0.0, -166.15942) MPa on face 337: plane, area 6720.00 mm^2, centroid (29938.0, 522.5, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (4) uniform traction (-0.0, 0.0, -166.15942) MPa on face 304: plane, area 6720.00 mm^2, centroid (62.0, 227.5, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (5) uniform traction (-0.0, 0.0, -166.15942) MPa on face 306: plane, area 360.00 mm^2, centroid (62.0, 375.0, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (6) uniform traction (-0.0, 0.0, -166.15942) MPa on face 309: plane, area 6720.00 mm^2, centroid (62.0, 522.5, 2100.0) mm, outward normal (0.0, 0.0, 1.0). (7) uniform traction (0.0, 0.0, 30.204082) MPa on face 240: plane, area 30625.00 mm^2, centroid (9350.0, 375.0, -50.0) mm, outward normal (-0.0, -0.0, -1.0). (8) uniform traction (0.0, 0.0, 30.204082) MPa on face 610: plane, area 30625.00 mm^2, centroid (20650.0, 375.0, -50.0) mm, outward normal (-0.0, -0.0, -1.0). (9) uniform traction (-0.0, -0.0, 5.423191) MPa on face 240: plane, area 30625.00 mm^2, centroid (9350.0, 375.0, -50.0) mm, outward normal (-0.0, -0.0, -1.0). (10) uniform traction (-0.0, -0.0, 5.423191) MPa on face 286: plane, area 225.00 mm^2, centroid (1550.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (11) uniform traction (-0.0, -0.0, 5.423191) MPa on face 320: plane, area 360.00 mm^2, centroid (62.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (12) uniform traction (-0.0, -0.0, 5.423191) MPa on face 348: plane, area 360.00 mm^2, centroid (29938.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (13) uniform traction (-0.0, -0.0, 5.423191) MPa on face 376: plane, area 225.00 mm^2, centroid (5450.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (14) uniform traction (-0.0, -0.0, 5.423191) MPa on face 410: plane, area 225.00 mm^2, centroid (15000.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (15) uniform traction (-0.0, -0.0, 5.423191) MPa on face 478: plane, area 225.00 mm^2, centroid (24550.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (16) uniform traction (-0.0, -0.0, 5.423191) MPa on face 512: plane, area 225.00 mm^2, centroid (28450.0, 375.0, 0.0) mm, outward normal (0.0, 0.0, -1.0). (17) uniform traction (-0.0, -0.0, 5.423191) MPa on face 584: plane, area 22027.50 mm^2, centroid (808.25, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (18) uniform traction (-0.0, -0.0, 5.423191) MPa on face 585: plane, area 58275.00 mm^2, centroid (3500.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (19) uniform traction (-0.0, -0.0, 5.423191) MPa on face 586: plane, area 57075.00 mm^2, centroid (7360.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (20) uniform traction (-0.0, -0.0, 5.423191) MPa on face 587: plane, area 83325.00 mm^2, centroid (12215.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (21) uniform traction (-0.0, -0.0, 5.423191) MPa on face 588: plane, area 83325.00 mm^2, centroid (17785.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (22) uniform traction (-0.0, -0.0, 5.423191) MPa on face 591: plane, area 57075.00 mm^2, centroid (22640.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (23) uniform traction (-0.0, -0.0, 5.423191) MPa on face 592: plane, area 58275.00 mm^2, centroid (26500.0, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (24) uniform traction (-0.0, -0.0, 5.423191) MPa on face 593: plane, area 22027.50 mm^2, centroid (29191.75, 375.0, 0.0) mm, outward normal (-0.0, -0.0, -1.0). (25) uniform traction (-0.0, -0.0, 5.423191) MPa on face 610: plane, area 30625.00 mm^2, centroid (20650.0, 375.0, -50.0) mm, outward normal (-0.0, -0.0, -1.0). No self-weight.
Analysis: compute the linear prebuckling stress state under the reference load set, then the elastic buckling load factors lambda (eigenvalues of K + lambda K_G = 0, the whole reference load set scaled by lambda). Report the smallest positive one.

Outputs:
- lambda1 [-]: first (smallest positive) elastic buckling load factor of the reference load set

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
