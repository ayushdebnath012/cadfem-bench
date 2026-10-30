# A-RIGGING-test1

**Load test 1: the plate is pulled through its holes with 12.0 kN. What is the highest stress in it?**

Family: Aluminium rigging plate · Set: Main · Physics: Stress and bending · Track A: the CAD file is given

## Overview

A 7075 aluminium plate that connects lifting slings. It is pulled through its holes exactly as in the maker's own load tests.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (riggingplate.step, boundary-conditions.png).
2. Load riggingplate.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_von_mises_MPa, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from ANSYS Mechanical (the maker's stress plots); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `riggingplate.step` | 3D CAD file |
| `boundary-conditions.png` | Figure |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "max_von_mises_MPa": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `max_von_mises_MPa` | MPa | maximum equivalent (von Mises) stress in the plate |

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
| `max_von_mises_MPa` | \|answer − reference\| / \|reference\| ≤ 20 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: max_von_mises_MPa | Highest stress (von Mises) is outside ±20 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_von_mises_MPa. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by ANSYS Mechanical (the maker's stress plots); source: [OpenRiggingPlate (mpangch)](https://github.com/mpangch/OpenRiggingPlate).

## Exact prompt

```text
Hard-anodised 7075-T6 rigging plate, load test 1 of the source's seven ANSYS load cases (Test 1 (2697.7 lbf)). riggingplate.step is the single solid in millimetres (235.58 x 111.90 x 12 mm, 145 faces).
Material: aluminium 7075-T6, linear isotropic elastic (standard handbook values; the source did not publish its card, and the graded stress does not depend on Young's modulus for these loads).
Analysis: linear static, small displacements (ANSYS Mechanical in the source).
Boundary conditions: exactly as shown in boundary-conditions.png (the source's own ANSYS figure): each labelled scope (A, B, ...) is a face or set of faces of the plate; 'Force' applies the stated total force uniformly distributed over the scoped faces in the drawn direction; 'Remote Displacement' fixes the scoped faces through a rigid remote point (all displacements and rotations zero). Where only two equal and opposite forces are applied and no support is drawn, the plate is self-equilibrated; remove rigid-body motion without adding load (e.g. weak springs or inertia relief), as the source did.
Legend of this test's figure: A Force: 12000 N; B; Force 2: 12000 N.

Outputs:
- max_von_mises_MPa [MPa]: maximum equivalent (von Mises) stress in the plate

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
