# B-RIGGING-test1

**Load test 1 again, but the model gets only the maker's drawing and has to build the CAD itself. What is the highest stress in the plate?**

Family: Aluminium rigging plate · Set: Main · Physics: Stress and bending · Track B: the model builds the CAD from the description

## Overview

A 7075 aluminium plate that connects lifting slings. It is pulled through its holes exactly as in the maker's own load tests.

Analysis: linear static elasticity: K·u = f with the given supports and loads.

## Flow

1. Read the prompt and the input files (rigging-plate-drawing.pdf, boundary-conditions.png).
2. Build the part described in the prompt with CadQuery, in the stated coordinate frame (cracks go into the mesh), and export it as part.step. Figures and drawings are for reading the shape, not CAD.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity: K·u = f with the given supports and loads. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into max_von_mises_MPa, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from ANSYS Mechanical (the maker's stress plots); check the files and the shape, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `rigging-plate-drawing.pdf` | Drawing |
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
| Shape | same number of solids as the reference; \|ΔV\| / V ≤ 2 %; aligned to the reference before comparison |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, the shape gate passed, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid, shape matches and the expert annotators signed off. |
| Wrong number: max_von_mises_MPa | Highest stress (von Mises) is outside ±20 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: max_von_mises_MPa. |
| Shape not exact | part.step differs from the reference shape: a different number of solids, volume off by more than 2 %, or surface more than max(0.5 mm, 0.1 % of the diagonal) away. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by ANSYS Mechanical (the maker's stress plots); source: [OpenRiggingPlate (mpangch)](https://github.com/mpangch/OpenRiggingPlate).

## Exact prompt

```text
Hard-anodised 7075-T6 rigging plate, load test 1 of the source's seven ANSYS load cases (Test 1 (2697.7 lbf)). Build the plate yourself from rigging-plate-drawing.pdf (the source's dimensioned manufacturing drawing, millimetres, 12 mm thick, all seams blended) and export it as part.step; then analyse your own model.
Material: aluminium 7075-T6, linear isotropic elastic (standard handbook values; the source did not publish its card, and the graded stress does not depend on Young's modulus for these loads).
Analysis: linear static, small displacements (ANSYS Mechanical in the source).
Boundary conditions: exactly as shown in boundary-conditions.png (the source's own ANSYS figure): each labelled scope (A, B, ...) is a face or set of faces of the plate; 'Force' applies the stated total force uniformly distributed over the scoped faces in the drawn direction; 'Remote Displacement' fixes the scoped faces through a rigid remote point (all displacements and rotations zero). Where only two equal and opposite forces are applied and no support is drawn, the plate is self-equilibrated; remove rigid-body motion without adding load (e.g. weak springs or inertia relief), as the source did.
Legend of this test's figure: A Force: 12000 N; B; Force 2: 12000 N.
Model the plate with its length, width and 12 mm thickness along the coordinate axes; any position and any of the 24 axis-aligned orientations is accepted: the evaluator aligns part.step to the original CAD (bounding-box centres, proper axis rotations; mirror images are not accepted) before measuring volume overlap, and separately reviews drawing features and boundary-condition mapping.

Outputs:
- max_von_mises_MPa [MPa]: maximum equivalent (von Mises) stress in the plate

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
