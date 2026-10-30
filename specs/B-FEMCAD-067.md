# B-FEMCAD-067

**A thick-walled tube heated on a band of its inner wall. What temperature does a probe point reach?**

Family: Build it from a description · Set: Main · Physics: Heat · Track B: the model builds the CAD from the description

## Overview

No CAD file is given. The model reads a written description, builds the part itself, then analyses it.

Analysis: heat conduction: temperature field from the given heating and boundary conditions.

## Flow

1. Read the prompt and the input files (figure-1.gif).
2. Build the part described in the prompt with CadQuery, in the stated coordinate frame (cracks go into the mesh), and export it as part.step. Figures and drawings are for reading the shape, not CAD.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: heat conduction: temperature field from the given heating and boundary conditions. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into T_probe_K, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Wolfram (Mathematica) FEM verification tests; check the files and the shape, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `figure-1.gif` | Figure |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "T_probe_K": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `T_probe_K` | K | temperature at (r, z) = (40, 40) |

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
| `T_probe_K` | \|answer − reference\| / \|reference\| ≤ 1 % |
| Shape | same number of solids as the reference; \|ΔV\| / V ≤ 2 %; aligned to the reference before comparison |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, the shape gate passed, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid, shape matches and the expert annotators signed off. |
| Wrong number: T_probe_K | Temperature at the probe point is outside ±1 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: T_probe_K. |
| Shape not exact | part.step differs from the reference shape: a different number of solids, volume off by more than 2 %, or surface more than max(0.5 mm, 0.1 % of the diagonal) away. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Wolfram (Mathematica) FEM verification tests; source: [Wolfram FEM documentation: Heat Transfer Verification Tests](https://reference.wolfram.com/language/PDEModels/tutorial/HeatTransfer/HeatTransferVerificationTests.html).

## Exact prompt

```text
CAD + FEM task. Build the part with a CAD script and write it as part.step in millimetres in exactly the coordinate frame given (multi-region models: one STEP with one solid per region and shared, coincident interface faces; 2-D models: planar faces in the z = 0 plane); then analyse YOUR model with any open-source FEM library, set up exactly as under Analysis. main.py must run both steps (artifact contract below). Report mesh-converged values (each changes by less than 1 % under refinement). Your results are compared with the reference analysis.

Geometry. Tube about z, units mm: inner radius 20, outer radius 100, z in [0, 140]; split the bore surface at z = 40 and z = 100 so the heated band is its own face.

Analysis. Steady conduction, k = 52 W/(m K). Heat flux 5e5 W/m^2 into the solid through the bore band 40 <= z <= 100; T = 273.15 K on z = 0, z = 140 and r = 100; the rest of the bore insulated.
The evaluator aligns part.step to a reference solid built from this specification (bounding-box centres, the 24 proper axis rotations; mirror images are not accepted) and requires a relative symmetric volume difference of at most 2 %; it separately reviews features, regions and boundary-condition faces.

Outputs:
- T_probe_K [K]: temperature at (r, z) = (40, 40)

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
