# A-MORPHWING-Test2

**Test 2: a uniform 4 mm plate, clamped at one end. How fast does it vibrate when it flaps, twists, and flaps in an S-shape?**

Family: Morphing-wing test plates · Set: Main · Physics: Vibration · Track A: the CAD file is given

## Overview

3D-printed PLA plates from a study of wings that change shape. Each plate is clamped at one end like a diving board.

Analysis: modal analysis: natural frequencies of the clamped structure from K·φ = ω²·M·φ, modes identified by shape.

## Flow

1. Read the prompt and the input files (part.step).
2. Load part.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: modal analysis: natural frequencies of the clamped structure from K·φ = ω²·M·φ, modes identified by shape. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into f_1B_Hz, f_1T_Hz, f_2B_Hz, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Abaqus shell model (the study's open data); check the files, and expert human annotators verify the CAD and sign off the workflow.

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
    "f_1B_Hz": <number>,
    "f_1T_Hz": <number>,
    "f_2B_Hz": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `f_1B_Hz` | Hz | first out-of-plane bending mode |
| `f_1T_Hz` | Hz | first torsion mode about the span (x) axis |
| `f_2B_Hz` | Hz | second out-of-plane bending mode |

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
| `f_1B_Hz` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `f_1T_Hz` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `f_2B_Hz` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: f_1B_Hz | 1st flapping (bending) frequency is outside ±5 % of the reference. |
| Wrong number: f_1T_Hz | 1st twisting frequency is outside ±5 % of the reference. |
| Wrong number: f_2B_Hz | 2nd bending frequency is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: f_1B_Hz, f_1T_Hz, f_2B_Hz. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Abaqus shell model (the study's open data); source: [Experimental and numerical data of candidate structural models for active camber morphing wings (Huang & Zhang)](https://data.mendeley.com/datasets/8jxw5533py/1).

## Exact prompt

```text
Cantilever plate specimen for an active-camber morphing-wing study (FDM-printed PLA): a uniform 4 mm plate. part.step is one solid in millimetres, 144 x 50 x 4 mm, with a 19 mm clamping grip at x = 0-19 mm (the scalloped clamp region).
Model the vibrating structure only: the free part x >= 19 mm, clamped (all displacements and rotations zero) along its whole cross-section at x = 19 mm. The grip is held in the fixture and is not part of the model.
Material: PLA treated as isotropic linear elastic, E = 2107 MPa, Poisson ratio 0.3, density 1180 kg/m^3.
Analysis: undamped natural frequencies (modal analysis), no prestress, no gravity. Identify the modes by their shapes.

Outputs:
- f_1B_Hz [Hz]: first out-of-plane bending mode
- f_1T_Hz [Hz]: first torsion mode about the span (x) axis
- f_2B_Hz [Hz]: second out-of-plane bending mode

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
