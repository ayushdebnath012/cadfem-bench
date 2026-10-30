# B-CA-SSLS120

**An open cylindrical tank full of water. How much does the wall bulge at the base, how far does the top rim move, and how high is the wall stress at the base?**

Family: Pipe elbow and water tank (Code_Aster) · Set: Main · Physics: Stress and bending · Track B: the model builds the CAD from the description

## Overview

Two classic pressure-equipment problems from the Code_Aster validation suite, built from a description.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (figure-1.png).
2. Build the part described in the prompt with CadQuery, in the stated coordinate frame (cracks go into the mesh), and export it as part.step. Figures and drawings are for reading the shape, not CAD.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into u_r_base_mm, u_z_top_mm, sigma_hoop_base_MPa, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Code_Aster validation documents (published reference solution); check the files and the shape, and expert human annotators verify the CAD and sign off the workflow.

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
    "u_r_base_mm": <number>,
    "u_z_top_mm": <number>,
    "sigma_hoop_base_MPa": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `u_r_base_mm` | mm | radial displacement of the mid-surface at z = 0 |
| `u_z_top_mm` | mm | axial displacement of the mid-surface at z = 16000 |
| `sigma_hoop_base_MPa` | MPa | hoop stress on the mid-surface at z = 0 |

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
| `u_r_base_mm` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `u_z_top_mm` | \|answer − reference\| / \|reference\| ≤ 5 % |
| `sigma_hoop_base_MPa` | \|answer − reference\| / \|reference\| ≤ 5 % |
| Shape | same number of solids as the reference; \|ΔV\| / V ≤ 2 %; Hausdorff distance ≤ max(0.5 mm, 0.1 % of the reference diagonal); in the given coordinate frame, no re-alignment |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, the shape gate passed, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid, shape matches and the expert annotators signed off. |
| Wrong number: u_r_base_mm | Outward bulge of the wall at the base is outside ±5 % of the reference. |
| Wrong number: u_z_top_mm | Vertical movement of the top rim is outside ±5 % of the reference. |
| Wrong number: sigma_hoop_base_MPa | Hoop stress in the wall at the base is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: u_r_base_mm, u_z_top_mm, sigma_hoop_base_MPa. |
| Shape not exact | part.step differs from the reference shape: a different number of solids, volume off by more than 2 %, or surface more than max(0.5 mm, 0.1 % of the diagonal) away. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Code_Aster validation documents (published reference solution); source: [Code_Aster validation test SSLS120](https://codeaster.gitlab.io/doc/docaster/manuals/man_v/v3/v3.03.120/index.html).

## Exact prompt

```text
CAD + FEM task. Build the part with a CAD script and write it as part.step in millimetres in exactly the coordinate frame given (assemblies: one STEP with one solid per body); then analyse YOUR model with any open-source FEM library, set up exactly as under Analysis. main.py must run both steps (artifact contract below). Report mesh-converged values (each changes by less than 1 % under refinement) and record at least three mesh levels in refinement.json. Your results are compared with the published reference analysis.

Geometry (mm). One solid: a cylindrical wall of mean radius 5700 and thickness 40 (radii 5680 to 5720), axis z, 0 <= z <= 16000, open at both ends.

Analysis. Linear elasticity: E = 210000 MPa, Poisson ratio 0.3. Simply supported base with free rotation: only the axial displacement of the mid-surface circle r = 5700, z = 0 is prevented (plus minimal restraint of rigid rotation about z). Internal hydrostatic pressure on the inner face p(z) = 0.015 (16000 - z) / 16000 MPa. Report, on the mid-surface, the radial displacement at z = 0, the axial displacement at z = 16000, and the hoop stress at z = 0.

The evaluator compares part.step with a reference solid built from this specification, in the given frame and without re-alignment: same number of solids, volume within 2 %, and Hausdorff surface distance at most max(0.5 mm, 0.1 % of the reference bounding-box diagonal). It separately reviews features, regions and boundary-condition faces.

Outputs:
- u_r_base_mm [mm]: radial displacement of the mid-surface at z = 0
- u_z_top_mm [mm]: axial displacement of the mid-surface at z = 16000
- sigma_hoop_base_MPa [MPa]: hoop stress on the mid-surface at z = 0

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
