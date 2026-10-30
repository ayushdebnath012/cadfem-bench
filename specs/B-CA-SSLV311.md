# B-CA-SSLV311

**A thick steel disc spinning at 500 rad/s with a small quarter-ellipse crack at the edge of its central hole. How hard is the crack pulled open at two points along its edge?**

Family: Cracks (Code_Aster tests) · Set: Main · Physics: Cracks · Track B: the model builds the CAD from the description

## Overview

Classic crack problems from the Code_Aster validation suite. The model builds the cracked part from a description and finds the stress intensity factors, the numbers engineers use to predict whether a crack will grow.

Analysis: linear elastic fracture: a static solve with the crack in the mesh, then stress intensity factors or energy release rate at the crack front (J-integral, G-theta or displacement correlation).

## Flow

1. Read the prompt and the input files (figure-1.png).
2. Build the part described in the prompt with CadQuery, in the stated coordinate frame (cracks go into the mesh), and export it as part.step. Figures and drawings are for reading the shape, not CAD.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear elastic fracture: a static solve with the crack in the mesh, then stress intensity factors or energy release rate at the crack front (J-integral, G-theta or displacement correlation). Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into K_I_s05_MPa_sqrt_m, K_I_s34_MPa_sqrt_m, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Code_Aster validation documents (exact formula or ANSYS result); check the files and the shape, and expert human annotators verify the CAD and sign off the workflow.

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
    "K_I_s05_MPa_sqrt_m": <number>,
    "K_I_s34_MPa_sqrt_m": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `K_I_s05_MPa_sqrt_m` | MPa·√m | K_I at front arc length 5.349 mm from the bore end |
| `K_I_s34_MPa_sqrt_m` | MPa·√m | K_I at front arc length 34.448 mm from the bore end |

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
| `K_I_s05_MPa_sqrt_m` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `K_I_s34_MPa_sqrt_m` | \|answer − reference\| / \|reference\| ≤ 10 % |
| Shape | same number of solids as the reference; \|ΔV\| / V ≤ 2 %; Hausdorff distance ≤ max(0.5 mm, 0.1 % of the reference diagonal); in the given coordinate frame, no re-alignment |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, the shape gate passed, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid, shape matches and the expert annotators signed off. |
| Wrong number: K_I_s05_MPa_sqrt_m | Crack opening intensity K_I, 5.3 mm along the crack edge is outside ±10 % of the reference. |
| Wrong number: K_I_s34_MPa_sqrt_m | Crack opening intensity K_I, 34.4 mm along the crack edge is outside ±10 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: K_I_s05_MPa_sqrt_m, K_I_s34_MPa_sqrt_m. |
| Shape not exact | part.step differs from the reference shape: a different number of solids, volume off by more than 2 %, or surface more than max(0.5 mm, 0.1 % of the diagonal) away. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Code_Aster validation documents (exact formula or ANSYS result); source: [Code_Aster validation test SSLV311](https://codeaster.gitlab.io/doc/docaster/manuals/man_v/v3/v3.04.311/index.html).

## Exact prompt

```text
CAD + FEM task. Build the part with a CAD script and write it as part.step in millimetres in exactly the coordinate frame given (assemblies: one STEP with one solid per body); then analyse YOUR model with any open-source FEM library, set up exactly as under Analysis. main.py must run both steps (artifact contract below). Report mesh-converged values (each changes by less than 1 % under refinement) and record at least three mesh levels in refinement.json. Your results are compared with the published reference analysis.

Geometry (mm). One solid: an annular disc with axis z, inner (bore) radius 100, outer radius 600, 0 <= z <= 200. A quarter-elliptical corner crack lies in the half-plane y = 0, x > 0, at the corner between the bore (r = 100) and the face z = 0: its front is x = 100 + 12.5 sin(theta), z = 50 cos(theta), 0 <= theta <= 90 deg (axial semi-axis 50 along the bore, radial semi-axis 12.5 on the face z = 0). part.step is the uncracked disc; insert the crack in your mesh.

Analysis. Linear elasticity: E = 200000 MPa, Poisson ratio 0.3, density 7800 kg/m^3. The disc rotates steadily about z at 500 rad/s (centrifugal body force only; no other load). Suppress rigid-body motion minimally so that the result is unaffected. Compute the mode-I stress intensity factor K_I along the crack front by a FEM fracture method (J-integral/G-theta, displacement correlation with singular or quarter-point elements, etc.). Report K_I at the two front points located by arc length s measured along the front from its bore end (100, 0, 50) (front length 53.62 mm): s = 5.349 mm, i.e. point (104.225, 0, 47.058), and s = 34.448 mm, i.e. point (111.548, 0, 19.135).

The evaluator compares part.step with a reference solid built from this specification, in the given frame and without re-alignment: same number of solids, volume within 2 %, and Hausdorff surface distance at most max(0.5 mm, 0.1 % of the reference bounding-box diagonal). It separately reviews features, regions and boundary-condition faces.

Outputs:
- K_I_s05_MPa_sqrt_m [MPa*m^0.5]: K_I at front arc length 5.349 mm from the bore end
- K_I_s34_MPa_sqrt_m [MPa*m^0.5]: K_I at front arc length 34.448 mm from the bore end

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
