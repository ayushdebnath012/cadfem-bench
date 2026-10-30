# A-FCVM-PL-Wyk_Rohrstoss_ring

**A steel pipe-joint ring held at its bosses and loaded. How many times the given load can it carry before it collapses?**

Family: Steel parts at collapse (fcVM) · Set: Main · Physics: Collapse · Track A: the CAD file is given

## Overview

Steel parts loaded until the metal yields right through and they can carry no more.

Analysis: plastic collapse: elastic-perfectly plastic material, load increased until the structure can carry no more (limit load factor).

## Flow

1. Read the prompt and the input files (analysis.step, faces.json).
2. Load analysis.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them), then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: plastic collapse: elastic-perfectly plastic material, load increased until the structure can carry no more (limit load factor). Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into limit_load_factor, and check each changes by less than 1 % between the two finest meshes.
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
    "limit_load_factor": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `limit_load_factor` | - | plastic collapse (limit) load factor of the reference load set (how many times the given load the part carries when it collapses plastically) |

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
| `limit_load_factor` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: limit_load_factor | Collapse factor: how many times the given load it can carry is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: limit_load_factor. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by the fcVM FreeCAD workbench solver; source: [fcVM workbench examples (Harry van Langen, HarryvL/fcVM-workbench)](https://github.com/HarryvL/fcVM-workbench).

## Exact prompt

```text
Plastic collapse (limit load) analysis of a steel part from the fcVM workbench examples (Wyk_Rohrstoss_ring). analysis.step holds the analysis geometry in millimetres (12 solid region(s) that share their interfaces and act as one continuous body, volume 2577880 mm^3). faces.json describes every face (index, type, area, centroid, normal/axis).
Material: elastic-perfectly plastic von Mises (associated flow, no hardening), E = 210000 MPa, Poisson ratio 0.3, yield stress 235 MPa. Small strains and small displacements (geometrically linear).
Supports: (1) all displacement components = 0 on face 5: cylinder, area 879.65 mm^2, centroid (105.0, -105.0, 10.0) mm, radius 7.0 mm, axis (-0.0, -0.0, -1.0) through (105.0, -105.0, 0.0) (boss/shaft surface); face 6: cylinder, area 879.65 mm^2, centroid (-105.0, -105.0, 10.0) mm, radius 7.0 mm, axis (-0.0, -0.0, -1.0) through (-105.0, -105.0, 0.0) (boss/shaft surface); face 7: cylinder, area 879.65 mm^2, centroid (105.0, 105.0, 10.0) mm, radius 7.0 mm, axis (-0.0, -0.0, -1.0) through (105.0, 105.0, 0.0) (boss/shaft surface); face 8: cylinder, area 879.65 mm^2, centroid (-105.0, 105.0, 10.0) mm, radius 7.0 mm, axis (-0.0, -0.0, -1.0) through (-105.0, 105.0, 0.0) (boss/shaft surface).
Reference load set (load factor 1): (1) uniform traction (0.0, 0.0, 43.521099) MPa on face 49: plane, area 1501.11 mm^2, centroid (-45.962, 45.962, 390.0) mm, outward normal (-0.7071, 0.7071, -0.0). (2) uniform traction (-0.0, -0.0, -43.521099) MPa on face 52: plane, area 1501.11 mm^2, centroid (45.962, -45.962, 390.0) mm, outward normal (0.7071, -0.7071, -0.0). (3) uniform traction (0.213062, -0.213062, 0.0) MPa on face 55: plane, area 14635.83 mm^2, centroid (-0.0, -0.0, 400.0) mm, outward normal (0.0, 0.0, 1.0). No self-weight.
Analysis: scale the whole reference load set proportionally by a load factor lambda and find the plastic collapse (limit) load factor, the largest lambda for which equilibrium exists (the load-displacement curve becomes flat).

Outputs:
- limit_load_factor [-]: plastic collapse (limit) load factor of the reference load set

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
