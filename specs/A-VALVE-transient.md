# A-VALVE-transient

**Hot fluid suddenly flows through the valve. What are the largest and smallest temperature differences across the wall at two sections, and how hot is the outer wall there after 100 seconds?**

Family: Power-plant valve heating up · Set: Main · Physics: Heat · Track A: the CAD file is given

## Overview

A valve in a power plant: a carbon-steel nozzle welded to stainless-steel bodies. Hot fluid suddenly flows through. The steel's properties change with temperature.

Analysis: nonlinear transient heat conduction: time stepping with temperature-dependent properties.

## Flow

1. Read the prompt and the input files (valve.brep, asme-properties.fee, internal-temperature.csv, faces.json, valve-surfaces.png, valve-materials.png).
2. Load valve.brep with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them), then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: nonlinear transient heat conduction: time stepping with temperature-dependent properties. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into scl2_dT_max_K, scl2_dT_min_K, scl4_dT_max_K, scl4_dT_min_K, scl2_T_outer_100s_C, scl4_T_outer_100s_C, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from FeenoX (tutorial results); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `valve.brep` | 3D CAD file |
| `asme-properties.fee` | Data file |
| `internal-temperature.csv` | Data file |
| `faces.json` | Face list |
| `valve-surfaces.png` | Figure |
| `valve-materials.png` | Figure |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "scl2_dT_max_K": <number>,
    "scl2_dT_min_K": <number>,
    "scl4_dT_max_K": <number>,
    "scl4_dT_min_K": <number>,
    "scl2_T_outer_100s_C": <number>,
    "scl4_T_outer_100s_C": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `scl2_dT_max_K` | K | maximum over time of T(inner end) - T(outer end) on SCL2 (heat-up) |
| `scl2_dT_min_K` | K | minimum over time of T(inner end) - T(outer end) on SCL2 (cool-down, negative) |
| `scl4_dT_max_K` | K | maximum over time of T(inner) - T(outer) on SCL4 |
| `scl4_dT_min_K` | K | minimum over time of T(inner) - T(outer) on SCL4 |
| `scl2_T_outer_100s_C` | °C | temperature at the outer end of SCL2 at t = 99.936 s |
| `scl4_T_outer_100s_C` | °C | temperature at the outer end of SCL4 at t = 99.936 s |

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
| `scl2_dT_max_K` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `scl2_dT_min_K` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `scl4_dT_max_K` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `scl4_dT_min_K` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `scl2_T_outer_100s_C` | \|answer − reference\| / \|reference − 40\| ≤ 5 % |
| `scl4_T_outer_100s_C` | \|answer − reference\| / \|reference − 40\| ≤ 5 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: scl2_dT_max_K | Largest temperature difference across the wall, section 2 is outside ±10 % of the reference. |
| Wrong number: scl2_dT_min_K | Most negative temperature difference, section 2 is outside ±10 % of the reference. |
| Wrong number: scl4_dT_max_K | Largest temperature difference across the wall, section 4 is outside ±10 % of the reference. |
| Wrong number: scl4_dT_min_K | Most negative temperature difference, section 4 is outside ±10 % of the reference. |
| Wrong number: scl2_T_outer_100s_C | Outer-wall temperature after 100 s, section 2 is outside ±5 % (+40 offset) of the reference. |
| Wrong number: scl4_T_outer_100s_C | Outer-wall temperature after 100 s, section 4 is outside ±5 % (+40 offset) of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: scl2_dT_max_K, scl2_dT_min_K, scl4_dT_max_K, scl4_dT_min_K, scl2_T_outer_100s_C, scl4_T_outer_100s_C. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by FeenoX (tutorial results); source: [FeenoX tutorial #3: heat conduction (valve with carbon and stainless steel parts)](https://www.seamplex.com/feenox/doc/tutorials/320-thermal/).

## Exact prompt

```text
Nonlinear transient heat conduction in a power-plant valve: a carbon-steel nozzle welded to stainless-steel valve bodies (half model, symmetry plane y = 0). valve.brep holds 4 solids in millimetres (112 faces). Solid 2 (the nozzle, x from 0 to 65 mm) is carbon steel; solids 1, 3 and 4 are stainless steel SA-312. faces.json lists every face with its index and its boundary group; valve-surfaces.png and valve-materials.png are the source's figures.

Materials: temperature-dependent conductivity k(T) and thermal diffusivity kappa(T) from asme-properties.fee (ASME II Part D tables, T in deg C): carbon steel uses k_carbon and kappa_carbon, stainless uses k_312 and kappa_312. As in the source, k from the tables is in W/(m K) and is multiplied by 1e-3 to W/(mm K); kappa is used as tabulated (mm^2/s). The volumetric heat capacity follows as k/kappa.
Boundary conditions: 'internal' faces: prescribed temperature T = Tint(t) from internal-temperature.csv (linear interpolation: 40 C at t = 0, 250 C from 100 s to 500 s, back to 40 C at 600 s, held to 1000 s). 'external' faces: convection h = 1e-6 W/(mm^2 K) to 50 C. 'symmetry' and both end faces: adiabatic.
Initial condition: the steady-state solution of the same problem at t = 0. Simulate 0 <= t <= 1000 s.
Stress classification lines: SCL2 (in the carbon-steel nozzle) runs from (3, 0, 48.5) mm on the inner wall to (3, 0, 57) mm on the outer wall; SCL4 (stainless body) from (-3, 0, 48.5) to (-3, 0, 57) mm.

Outputs:
- scl2_dT_max_K [K]: maximum over time of T(inner end) - T(outer end) on SCL2 (heat-up)
- scl2_dT_min_K [K]: minimum over time of T(inner end) - T(outer end) on SCL2 (cool-down, negative)
- scl4_dT_max_K [K]: maximum over time of T(inner) - T(outer) on SCL4
- scl4_dT_min_K [K]: minimum over time of T(inner) - T(outer) on SCL4
- scl2_T_outer_100s_C [C]: temperature at the outer end of SCL2 at t = 99.936 s
- scl4_T_outer_100s_C [C]: temperature at the outer end of SCL4 at t = 99.936 s

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
