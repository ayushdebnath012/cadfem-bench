# BT-i-section-03

**Steel I-section 30 × 30 mm (web 2, flanges 3), length 900 mm, clamped at one end, pushed along its length at the other. By what factor can the push change before it buckles?**

Family: Trap: I-beam · Set: Buckling traps · Physics: Buckling · Track A: the CAD file is given

## Overview

One of the 82 buckling-trap tasks: a simple metal part pushed along its length, with the push set above what it can take, so the true first buckling factor is below 1. An I-beam clamped at one end and pushed along its length at the other.

Analysis: linear buckling: a static solve under the given load, then the eigenvalue problem K + λ·K_G = 0 for the buckling factors.

## Flow

1. Read the prompt and the input files (analysis.step, faces.json).
2. Load analysis.step with CadQuery/OCP and find the faces named in the prompt by area, centroid and normal (faces.json lists them).
3. Mesh the solid with Gmsh (tetrahedra; quadratic elements recommended).
4. FEM solve inside main.py: linear buckling: a static solve under the given load, then the eigenvalue problem K + λ·K_G = 0 for the buckling factors. Material, supports and loads exactly as the prompt states. Solver: CalculiX 2.23 (ccx) or scikit-fem; the program writes the solver input itself.
5. Post-process the solver results into lambda1.
6. Write results.json and the other required files (main.py, solver.log) to CADFEM_OUTPUT_DIR.
7. Evaluation (by us, not the model): replay main.py once offline in the sandbox, then compare each value with the hidden reference from our FEniCSx model (quadratic elements, SLEPc eigen-solver, 3 meshes).

## Input

| File | What it is |
|---|---|
| prompt | the text below: geometry or CAD file name, material, supports, loads, analysis type, outputs |
| `analysis.step` | 3D CAD file |
| `faces.json` | Face list |

The model gets nothing else: no reference values, no internet, one attempt (600 s, 8 GiB, 2 threads).

## Output

`results.json` (plain JSON; replace each `<number>` with a number):

```
{
  "outputs": {
    "lambda1": <number>
  }
}
```

| Key | Unit | Meaning |
|---|---|---|
| `lambda1` | - | first positive buckling factor (the factor on the whole given load at which the part first buckles: 0.5 means it buckles at half the load, 2 at twice the load) |

Files to return:

| File | Must contain |
|---|---|
| `results.json` | the final numbers: {"outputs": {key: number}}, exactly the keys listed, plain JSON numbers |
| `main.py` | the whole program; runs end to end with no human help, reading CADFEM_INPUT_DIR and writing CADFEM_OUTPUT_DIR |
| `solver.log` | the FEM solver's own output, kept unedited |

## Evaluation

| Check | Rule |
|---|---|
| `lambda1` | \|answer − reference\| / \|reference\| ≤ 5 % |

**Pass:** λ₁ within ±5 % of the reference.

What the evaluator reports:

| Result | Meaning |
|---|---|
| Pass | every value within its band. |
| Wrong number: lambda1 | Buckling factor: how many times the given load makes it buckle is outside ±5 % of the reference. |
| No answer | results.json is missing, is not valid JSON, contains a non-finite number, or its keys are not exactly: lambda1. |
| Workflow incomplete | results.json, main.py or solver.log is missing or empty. |

## Reference answer

Hidden from the model. Computed by our FEniCSx model (quadratic elements, SLEPc eigen-solver, 3 meshes); source: evaluator-generated buckle-trap benchmark.

## Exact prompt

```text
Linear (eigenvalue) buckling analysis of a steel member: I-section 30 x 30 mm (web 2, flanges 3), length 900 mm. analysis.step holds the analysis geometry in millimetres (one solid). faces.json describes every face (index, type, area, centroid, normal/axis).
Material: linear isotropic elastic, E = 210000 MPa, Poisson ratio 0.3.
Supports: (1) all displacement components = 0 on face 13: plane, area 228.00 mm^2, centroid (0.0, 0.0, -0.0) mm, outward normal (-1.0, -0.0, -0.0).
Reference load set (load factor 1): (1) uniform traction (-75.8207, 0, 0) MPa on face 14: plane, area 228.00 mm^2, centroid (900.0, 0.0, -0.0) mm, outward normal (1.0, 0.0, 0.0). No self-weight.
Analysis: compute the linear prebuckling stress state under the reference load set, then the elastic buckling load factors lambda (eigenvalues of K + lambda K_G = 0, the whole reference load set scaled by lambda). Report the smallest positive one.

Outputs:
- lambda1 [-]: first (smallest positive) elastic buckling load factor of the reference load set

Submit results.json containing exactly an outputs object with this numeric key, plus main.py and solver.log.
```
