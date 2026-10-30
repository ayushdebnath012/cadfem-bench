# A-CADWORLD-001

**The aluminium part, 260 mm long, fixed at one end and pushed sideways with 200 N at the other. How far does it move, and how high do the stresses get?**

Family: Aluminium machine part (CADWorld) · Set: Main · Physics: Stress and bending · Track A: the CAD file is given

## Overview

A multi-feature aluminium part, fixed at one end and pushed sideways with 200 N at the other.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (part.step, faces.json, publisher-task-image.png).
2. Load part.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them), then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_displacement_mm, max_von_mises_MPa, max_shear_stress_MPa, max_principal_MPa, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from FreeCAD FEM with CalculiX (CADWorld); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `part.step` | 3D CAD file |
| `faces.json` | Face list |
| `publisher-task-image.png` | Figure |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "max_displacement_mm": <number>,
    "max_von_mises_MPa": <number>,
    "max_shear_stress_MPa": <number>,
    "max_principal_MPa": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `max_displacement_mm` | mm | maximum nodal displacement magnitude |
| `max_von_mises_MPa` | MPa | maximum nodal von Mises stress |
| `max_shear_stress_MPa` | MPa | maximum over nodes of (major principal stress - minor principal stress)/2; publisher CSV column Tresca Stress |
| `max_principal_MPa` | MPa | maximum nodal major principal stress |

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
| `max_von_mises_MPa` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `max_shear_stress_MPa` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `max_principal_MPa` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: max_displacement_mm | Biggest movement anywhere in the part is outside ±5 % of the reference. |
| Wrong number: max_von_mises_MPa | Highest stress (von Mises) is outside ±5 % of the reference. |
| Wrong number: max_shear_stress_MPa | Highest shear stress is outside ±5 % of the reference. |
| Wrong number: max_principal_MPa | Highest tensile stress is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_displacement_mm, max_von_mises_MPa, max_shear_stress_MPa, max_principal_MPa. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by FreeCAD FEM with CalculiX (CADWorld); source: [CADWorld FEM benchmark (Zdong104/CADWORLD; HF Zihan1004/CADWORLD)](https://github.com/Zdong104/CADWORLD).

## Exact prompt

```text
FreeCAD/CalculiX benchmark part (Multi-feature aluminium part, end load). part.step is the single solid in millimetres (38 faces, bounding box [-130.0, -0.0, -30.0, 130.0, 30.0, 30.0] mm). faces.json describes every face.

Material: AlMg3F24, linear isotropic elastic, E = 70000 MPa, Poisson ratio 0.3.
Analysis: linear static, small displacements, no gravity.
Supports: fixed (all displacement components zero) on face 6: plane, area 100.00 mm^2, centroid (-127.5, 0.0, 0.0) mm, outward normal (-0.0, -1.0, -0.0).
Load: total force 200 N along (0, 1, 0) applied uniformly over face 38: plane, area 100.00 mm^2, centroid (127.5, -0.0, 0.0) mm, outward normal (-0.0, -1.0, -0.0).
Mesh protocol of the publisher's reference solution (results are compared under this protocol): Gmsh 3-D mesh, first-order (linear) tetrahedra, maximum element size 2.0 mm, minimum 0.5 mm, CalculiX solver. Report nodal extrema of that solution.
The publisher column named Tresca Stress is maximum shear stress, (sigma1 - sigma3)/2. Report this half-difference as max_shear_stress_MPa, not the full principal-stress difference. This task reproduces the source linear model; it is not a validated physical strength assessment.

Outputs:
- max_displacement_mm [mm]: maximum nodal displacement magnitude
- max_von_mises_MPa [MPa]: maximum nodal von Mises stress
- max_shear_stress_MPa [MPa]: maximum over nodes of (major principal stress - minor principal stress)/2; publisher CSV column Tresca Stress
- max_principal_MPa [MPa]: maximum nodal major principal stress

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
