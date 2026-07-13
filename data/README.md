# Data Directory

This directory contains the input datasets required by the **Quantum Protein–Ligand Docking** framework.

The algorithm requires two comma-separated value (CSV) files:

- **protein.csv** – Protein interaction data
- **ligand.csv** – Ligand interaction data

These datasets are used during **Phase 1 (Classical Preprocessing)** to generate the encoded search space for the quantum search algorithm.

---

# Directory Structure

```text
data/

├── protein.csv
├── ligand.csv
└── README.md
```

---

# Overview

The proposed docking framework does **not** use the complete three-dimensional protein structure directly.

Instead, it operates on **interaction descriptors** extracted from the protein and ligand.

Currently, the implementation supports two interaction descriptors:

- Hydrophobic Interaction
- Hydrogen Bond Interaction

Each interaction site is represented as a numerical feature vector and later converted into binary and quantum representations during the encoding stages.

---

# Input Files

| File | Description |
|------|-------------|
| `protein.csv` | Protein interaction descriptors |
| `ligand.csv` | Ligand interaction descriptors |

Both files must follow the same column format.

---

# Protein Dataset

## Format

```csv
Site_ID,Hydrophobic,Hydrogen_Bond
P1,2.69,0.31
P2,2.28,0.13
P3,0.77,1.29
P4,1.15,0.87
...
```

---

## Columns

| Column | Description |
|---------|-------------|
| Site_ID | Unique identifier for each interaction site |
| Hydrophobic | Hydrophobic interaction score |
| Hydrogen_Bond | Hydrogen bond interaction score |

---

## Example

| Site_ID | Hydrophobic | Hydrogen_Bond |
|----------|------------:|--------------:|
| P1 | 2.69 | 0.31 |
| P2 | 2.28 | 0.13 |
| P3 | 0.77 | 1.29 |
| P4 | 1.15 | 0.87 |

---

# Ligand Dataset

## Format

```csv
Site_ID,Hydrophobic,Hydrogen_Bond
L1,2.69,0.31
L2,2.28,0.13
L3,0.77,1.29
```

---

## Columns

| Column | Description |
|---------|-------------|
| Site_ID | Unique identifier for each ligand interaction site |
| Hydrophobic | Hydrophobic interaction score |
| Hydrogen_Bond | Hydrogen bond interaction score |

---

## Example

| Site_ID | Hydrophobic | Hydrogen_Bond |
|----------|------------:|--------------:|
| L1 | 2.69 | 0.31 |
| L2 | 2.28 | 0.13 |
| L3 | 0.77 | 1.29 |

---

# Interaction Descriptors

The current implementation uses two physicochemical interaction descriptors.

## Hydrophobic Interaction

Represents the hydrophobic affinity at an interaction site.

Higher values generally indicate stronger hydrophobic interactions.

---

## Hydrogen Bond Interaction

Represents the hydrogen-bonding capability of the interaction site.

These values are used during both

- First Encoding
- Second Encoding

to construct the quantum representations.

---

# Data Requirements

Before running the project, ensure that

- Each interaction site has a unique identifier.
- Hydrophobic and Hydrogen_Bond columns contain numeric values.
- No missing values are present.
- Protein and ligand files contain the same column names.
- The ligand contains at least one interaction site.
- The protein contains at least as many interaction sites as the ligand.

---

# Constraints

The current implementation assumes

- Continuous interaction values.
- Two interaction descriptors.
- One row corresponds to one interaction site.

Additional descriptors can be incorporated by extending the encoding pipeline.

---

# How the Data is Used

The datasets pass through the following pipeline:

```text
protein.csv
          │
          ▼
Dataset Validation
          │
          ▼
Threshold Computation
          │
          ▼
First Encoding
          │
          ▼
Protein Segmentation
          │
          ▼
Quantum Search
```

```text
ligand.csv
          │
          ▼
Dataset Validation
          │
          ▼
Threshold Computation
          │
          ▼
First Encoding
          │
          ▼
Target Bit String
```

---

# Replacing the Sample Data

To evaluate a different protein–ligand pair:

1. Replace the contents of `protein.csv` with the new protein interaction descriptors.
2. Replace the contents of `ligand.csv` with the new ligand interaction descriptors.
3. Keep the same column names.
4. Save the files in CSV format.
5. Run the complete pipeline:

```bash
python main.py
```

No changes to the source code are required.

---

# Notes

- The interaction values should be extracted using an external preprocessing pipeline or molecular interaction analysis tool.
- The framework is independent of the source of these interaction values, provided they follow the required CSV format.
- During execution, the raw interaction values are transformed into binary representations and subsequently into quantum amplitude vectors.

---

# Future Extensions

The current implementation supports two interaction descriptors.

Future versions may include additional features such as:

- Electrostatic interactions
- van der Waals interactions
- Aromatic interactions
- Salt bridges
- π–π stacking interactions
- Solvent accessibility descriptors

These can be incorporated by extending the encoding stages while preserving the overall workflow.

---

# Related Documentation

For additional information, refer to:

- **Project Overview:** `../README.md`
- **Source Code Documentation:** `../src/README.md`
- **Output Files:** `../outputs/README.md`
- **Notebook Documentation:** `../notebooks/README.md`