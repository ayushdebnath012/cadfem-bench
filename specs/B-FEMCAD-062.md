# B-FEMCAD-062

**A 100 × 50 × 5 mm steel plate with a 20 mm hole, fixed at one end and pulled with 1000 N at the other. What is the highest stress?**

Family: Build it from a description · Set: Main · Physics: Stress and bending · Track B: the model builds the CAD from the description

## Overview

No CAD file is given. The model reads a written description, builds the part itself, then analyses it.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (figure-1.png).
2. Build the part described in the prompt with CadQuery, in the stated coordinate frame (cracks go into the mesh), and export it as part.step. Figures and drawings are for reading the shape, not CAD.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_von_mises_MPa, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Wolfram (Mathematica) FEM verification tests; check the files and the shape, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `figure-1.png` | Figure |

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
| `max_von_mises_MPa` | MPa | maximum von Mises stress |

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
| `max_von_mises_MPa` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Shape | same number of solids as the reference; \|ΔV\| / V ≤ 2 %; aligned to the reference before comparison |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, the shape gate passed, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid, shape matches and the expert annotators signed off. |
| Wrong number: max_von_mises_MPa | Highest stress (von Mises) is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_von_mises_MPa. |
| Shape not exact | part.step differs from the reference shape: a different number of solids, volume off by more than 2 %, or surface more than max(0.5 mm, 0.1 % of the diagonal) away. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Wolfram (Mathematica) FEM verification tests; source: [Wolfram FEM documentation: Solid Mechanics Verification Tests](https://reference.wolfram.com/language/PDEModels/tutorial/StructuralMechanics/SolidMechanicsVerificationTests.html).

## Exact prompt

```text
CAD + FEM task. Build the part with a CAD script and write it as part.step in millimetres in exactly the coordinate frame given (multi-region models: one STEP with one solid per region and shared, coincident interface faces; 2-D models: planar faces in the z = 0 plane); then analyse YOUR model with any open-source FEM library, set up exactly as under Analysis. main.py must run both steps (artifact contract below). Report mesh-converged values (each changes by less than 1 % under refinement). Your results are compared with the reference analysis.

Geometry. Plate x in [0, 100], y in [0, 5], z in [0, 50] (units mm) with a through hole of radius 10 along y centred at (x, z) = (50, 25).

Analysis. E = 210000 MPa, Poisson ratio 0.3. Face x = 0 fixed; 1000 N in +x as a uniform traction on the face x = 100.
The evaluator aligns part.step to a reference solid built from this specification (bounding-box centres, the 24 proper axis rotations; mirror images are not accepted) and requires a relative symmetric volume difference of at most 2 %; it separately reviews features, regions and boundary-condition faces.

Outputs:
- max_von_mises_MPa [MPa]: maximum von Mises stress

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
