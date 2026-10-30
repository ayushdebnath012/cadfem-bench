# A-AGENTFEM-fresh_test_010

**Bracket design 010 (189 mm tall): feet fixed, seat pushed down with 10 kN. How far does the seat sink, and what is the biggest movement anywhere?**

Family: Double-arm support bracket · Set: Extra · Physics: Stress and bending · Track A: the CAD file is given

## Overview

An aluminium bracket that stands on two feet and holds a seat on top. Its feet are fixed to the floor and the seat is pushed down with 10 kN (about the weight of one tonne).

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (geometry.step).
2. Load geometry.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into seat_mean_displacement_mm, max_displacement_mm, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from the AgentFEM publisher's FEM run (quadratic tetrahedra, 9 mm mesh); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `geometry.step` | 3D CAD file |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "seat_mean_displacement_mm": <number>,
    "max_displacement_mm": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `seat_mean_displacement_mm` | mm | mean of the downward displacement -u_z over the top seat face (z = 189 mm) |
| `max_displacement_mm` | mm | maximum displacement magnitude anywhere in the bracket |

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
| `seat_mean_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: seat_mean_displacement_mm | How far the seat sinks, on average is outside ±10 % of the reference. |
| Wrong number: max_displacement_mm | Biggest movement anywhere in the part is outside ±10 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: seat_mean_displacement_mm, max_displacement_mm. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by the AgentFEM publisher's FEM run (quadratic tetrahedra, 9 mm mesh); source: [AgentFEM Bracket Elasticity (Haoming Luo, 2026)](https://huggingface.co/datasets/HaomingLuo/AgentFEM-Bracket-Elasticity).

## Exact prompt

```text
Support bracket (one member of a parametric double-arm bracket family). geometry.step holds one solid in millimetres (height 189 mm).

Material: linear isotropic elastic, E = 70 GPa, Poisson ratio 0.33 (density 2700 kg/m^3, gravity not applied).
Supports: the foot undersides, i.e. every face lying in the plane z = 0, are fully fixed (all displacement components zero).
Load: a uniform downward traction of 1.98728 MPa in the -z direction over the top seat face (the face in the plane z = 189 mm); total 10000 N.
Analysis: 3-D linear elasticity, small displacements. The publisher used quadratic tetrahedra with a nominal 9 mm mesh.

Outputs:
- seat_mean_displacement_mm [mm]: mean of the downward displacement -u_z over the top seat face (z = 189 mm)
- max_displacement_mm [mm]: maximum displacement magnitude anywhere in the bracket

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
