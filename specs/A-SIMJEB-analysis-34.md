# A-SIMJEB-analysis-34

**Competition entry #34, bolted down and pulled through its pin hole. How far does it move at most when pulled up, sideways, at 42 degrees and twisted?**

Family: Jet-engine lifting bracket · Set: Extra · Physics: Stress and bending · Track A: the CAD file is given

## Overview

In 2013 GE asked the public to design a lighter titanium bracket for lifting jet engines, and hundreds of designs came in. Each task is one real entry: bolted down at four holes and pulled through its pin hole in four separate ways (straight up, sideways, at 42 degrees, and twisted).

Analysis: linear static elasticity, solved separately for each load case.

## Flow

1. Read the prompt and the input files (bracket.step).
2. Load bracket.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal, then export the geometry analysed as part.step.
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended) at three or more sizes, so convergence can be shown.
4. FEM solve inside main.py: linear static elasticity, solved separately for each load case. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into vertical_max_displacement_mm, horizontal_max_displacement_mm, diagonal_max_displacement_mm, torsion_max_displacement_mm, and check each changes by less than 1 % between the two finest meshes.
6. Write results.json and the other required files (main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json, environment.json) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from Altair OptiStruct (SimJEB dataset); check the files, and expert human annotators verify the CAD and sign off the workflow.

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `bracket.step` | 3D CAD file |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "vertical_max_displacement_mm": <number>,
    "horizontal_max_displacement_mm": <number>,
    "diagonal_max_displacement_mm": <number>,
    "torsion_max_displacement_mm": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `vertical_max_displacement_mm` | mm | maximum displacement magnitude, vertical case |
| `horizontal_max_displacement_mm` | mm | maximum displacement magnitude, horizontal case |
| `diagonal_max_displacement_mm` | mm | maximum displacement magnitude, diagonal case |
| `torsion_max_displacement_mm` | mm | maximum displacement magnitude, torsion case |

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
| `vertical_max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `horizontal_max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `diagonal_max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| `torsion_max_displacement_mm` | \|answer − reference\| / \|reference\| ≤ 10 % |
| Files | all 8 files present and non-empty; part.step loads as a valid solid |
| Review | expert human annotators sign off execution, CAD geometry (features, regions, support and load faces), setup, field outputs and convergence against the file hashes |

**Pass:** Every output within its band, all 8 files present and part.step a valid solid, and expert human annotators sign off the CAD and the workflow.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band, all files present, part.step a valid solid and the expert annotators signed off. |
| Wrong number: vertical_max_displacement_mm | Biggest movement, pulled straight up is outside ±10 % of the reference. |
| Wrong number: horizontal_max_displacement_mm | Biggest movement, pulled sideways is outside ±10 % of the reference. |
| Wrong number: diagonal_max_displacement_mm | Biggest movement, pulled at 42 degrees is outside ±10 % of the reference. |
| Wrong number: torsion_max_displacement_mm | Biggest movement, twisted is outside ±10 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: vertical_max_displacement_mm, horizontal_max_displacement_mm, diagonal_max_displacement_mm, torsion_max_displacement_mm. |
| CAD not valid | part.step does not load as a valid solid. |
| Workflow incomplete | one of the 8 files is missing, empty or a link. |
| Not signed off | the expert human annotators found a problem with execution, the CAD geometry, setup, field outputs or convergence. |

## Reference answer

Hidden from the model. Computed by Altair OptiStruct (SimJEB dataset); source: [SimJEB: simulated jet engine bracket dataset (Whalen, Beyene, Mueller, CGF 2021) / GE bracket challenge](https://doi.org/10.7910/DVN/XFUWJG).

## Exact prompt

```text
Design task: the GE jet engine bracket. Units: millimetres, newtons, MPa. Material: Ti-6Al-4V (E = 113.8 GPa, nu = 0.342, density 4.43 g/cm^3, yield strength 903 MPa). The bracket is bolted to a flat mounting surface, the plane z = 0, with nothing below it, and carries a clevis for a pin.
Interfaces: (a) four vertical (+z) bolt holes of diameter 10.3124 mm (0.406 in) at (x, y) = (0.0000, 0.0000); (52.0472, 1.5805); (0.0000, -148.1248); (38.0833, -146.9684); each hole wall must start within 1.0 mm of z = 0 and be at least 5.5 mm long; the bolts are rigid and fully fixed. (b) a clevis of two lugs, each with a bore of diameter 19.1008 mm on the pin axis through (-20.9236, -74.6978, 44.7246) with direction (-0.030352, 0.999539, 0); measured along the axis from that point, the lug bores span 11.112 to 17.463 mm and -17.463 to -11.113 mm; the gap between the lugs must stay empty.
Design envelope: x -41 to 72, y -168 to 22, z 0 to 65 mm. Minimum wall / feature thickness 1.27 mm (at most 2 % of the surface may be thinner). One solid.
Loads, four separate linear static cases, each acting at the point (-21.0359, -75.0647, 44.8010) and spread over the two lug bores (RBE3): (1) vertical: 35,585.77 N along +z; (2) horizontal: 37,809.90 N along -x; (3) diagonal, 42 degrees from vertical: (-28,276.20, 0, 31,403.90) N; (4) torsion: 564,924.20 N mm about +z.
The attached STEP is a published competition design. Compute the maximum displacement magnitude for each of the four load cases. Targets are the original published OptiStruct displacement maxima; no locally computed stress target or pass verdict is scored.


Outputs:
- vertical_max_displacement_mm [mm]: maximum displacement magnitude, vertical case
- horizontal_max_displacement_mm [mm]: maximum displacement magnitude, horizontal case
- diagonal_max_displacement_mm [mm]: maximum displacement magnitude, diagonal case
- torsion_max_displacement_mm [mm]: maximum displacement magnitude, torsion case

Submit results.json containing exactly an outputs object with these numeric keys. Also submit main.py, part.step, mesh.msh, fields.npz, solver.log, refinement.json and environment.json. See candidate README for the artifact contract. Correct numerical answers alone do not establish workflow completion.
```
