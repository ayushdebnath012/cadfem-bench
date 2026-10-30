# A-GEOPINO-PLATE-8

**A 178 × 197 × 10 mm steel plate with a hole (case 8), fixed at one end and pushed with 1000 N at the other. How far does it move when pushed straight in, and when pushed sideways?**

Family: Steel plate with a hole · Set: Extra · Physics: Stress and bending · Track A: the CAD file is given

## Overview

A 10 mm steel plate with a hole through it, fixed along one end. The other end is pushed with 1000 N, first straight toward the fixed end, then sideways.

Analysis: linear static elasticity, solved separately for each of the two load cases.

## Flow

1. Read the prompt and the input files (part.step).
2. Load part.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity, solved separately for each of the two load cases. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_displacement_compression_mm, max_displacement_lateral_mm, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from ANSYS (GeoPINONet dataset); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `part.step` | 3D CAD file |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "max_displacement_compression_mm": <number>,
    "max_displacement_lateral_mm": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `max_displacement_compression_mm` | mm | maximum displacement magnitude, load case 1 |
| `max_displacement_lateral_mm` | mm | maximum displacement magnitude, load case 2 |

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
| `max_displacement_compression_mm` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `max_displacement_lateral_mm` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: max_displacement_compression_mm | Biggest movement when pushed straight in is outside ±5 % of the reference. |
| Wrong number: max_displacement_lateral_mm | Biggest movement when pushed sideways is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_displacement_compression_mm, max_displacement_lateral_mm. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by ANSYS (GeoPINONet dataset); source: [GeoPINONet holed-plate FEM dataset (Urrutia Valdes, La Fe-Perdomo, Rodriguez Soto)](https://zenodo.org/records/21483341).

## Exact prompt

```text
Holed steel plate. part.step is one solid in millimetres: a rectangular plate 178.440 mm (x) by 197.185 mm (y) by 10.000 mm (z) with a through hole along z.
Material: ANSYS default Structural Steel, linear isotropic elastic, E = 200 GPa, Poisson ratio 0.3. Linear static, small displacements, no gravity.
Supports: the end face at y = -98.5927 mm is fully fixed (all displacement components zero).
Two separate load cases, each a total force of 1000 N applied as a uniform traction over the opposite end face (y = 98.5927 mm):
  (1) compression: 1000 N along -y (towards the fixed end);
  (2) lateral bending: 1000 N along +x (in-plane shear of the free end).

Outputs:
- max_displacement_compression_mm [mm]: maximum displacement magnitude, load case 1
- max_displacement_lateral_mm [mm]: maximum displacement magnitude, load case 2

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
