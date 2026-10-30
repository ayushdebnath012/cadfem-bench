# A-NAFEMS-LE10

**A thick elliptical plate pressed on its top face (NAFEMS LE10), CAD supplied. What is the stress at point D?**

Family: Standard engineering tests (NAFEMS) · Set: Calibration · Physics: Stress and bending · Track A: the CAD file is given

## Overview

Textbook problems engineers use to check that simulation software works. These are warm-up tasks that a correct workflow should pass.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (input.json, part.step, published-geometry.geo, published-physics.txt, published-problem.png).
2. Load part.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into sigma_yy_at_D, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from NAFEMS target values; check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `input.json` | Data file |
| `part.step` | 3D CAD file |
| `published-geometry.geo` | 3D CAD file |
| `published-physics.txt` | Data file |
| `published-problem.png` | Drawing |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "sigma_yy_at_D": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `sigma_yy_at_D` | MPa | signed normal stress at the requested point (signed) |

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
| `sigma_yy_at_D` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: sigma_yy_at_D | Stress at point D is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: sigma_yy_at_D. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by NAFEMS target values; source: [FeenoX NAFEMS mechanical examples (seamplex/feenox)](https://www.seamplex.com/feenox/examples/mechanical.html).

## Exact prompt

```text
Use the supplied original STEP/Gmsh geometry definition; generate and refine your own analysis mesh.

The problem, material data, loads and constraints are supplied in published-problem.png, published-physics.txt and input.json. The text declarations are original source excerpts, not a solution program. In those declarations u/v/w denote x/y/z displacement. Pressure p is inward normal pressure; tension is outward normal traction. Units and the requested sampling point are in input.json.

Solve this physical problem using FEM. Save executable main.py, mesh.msh, field output (VTK/XDMF/NPZ), solver.log and refinement.json with at least two distinct mesh resolutions and the requested quantity at each. For cad_fem, export part.step. Include an explanation of formulation, physical setup and stress recovery. Do not return a recalled stress value without a solver workflow.

Requested quantity: signed normal stress 'sigma_yy_at_D' at the point [2000, 0, 300] (mm), reported in MPa. input.json gives units, the sampling point and source precision notes.

Outputs:
- sigma_yy_at_D [MPa]: signed normal stress at the requested point (signed)

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
