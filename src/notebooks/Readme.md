# Notebooks

The **notebooks** directory contains Jupyter notebooks used to develop, verify, and demonstrate each stage of the Quantum Protein–Ligand Docking framework.

Unlike the main implementation, which executes the complete pipeline automatically, these notebooks focus on individual components of the algorithm. They allow each stage to be studied, tested, and visualized independently.

These notebooks are intended for

- Learning the implementation
- Debugging individual modules
- Verifying mathematical derivations
- Testing intermediate outputs
- Demonstrating the algorithm step by step

---

# Directory Structure

```text
notebooks/

├── 01_First_Encoding.ipynb
├── 02_Protein_Segmentation.ipynb
├── 03_Amplitude_Vector.ipynb
├── 04_State_Preparation.ipynb
├── 05_Oracle.ipynb
├── 06_Diffusion.ipynb
├── 07_Grover_Search.ipynb
├── 08_Candidate_Evaluation.ipynb
├── 09_Second_Encoding.ipynb
├── 10_State_Construction.ipynb
├── 11_SWAP_Test.ipynb
└── README.md
```

---

# Notebook Workflow

```text
Protein & Ligand Data
          │
          ▼
01_First_Encoding
          │
          ▼
02_Protein_Segmentation
          │
          ▼
03_Amplitude_Vector
          │
          ▼
04_State_Preparation
          │
          ▼
05_Oracle
          │
          ▼
06_Diffusion
          │
          ▼
07_Grover_Search
          │
          ▼
08_Candidate_Evaluation
          │
          ▼
09_Second_Encoding
          │
          ▼
10_State_Construction
          │
          ▼
11_SWAP_Test
```

---

# Notebook Descriptions

## 01_First_Encoding.ipynb

### Purpose

Implements and verifies the first encoding stage.

### Demonstrates

- Dataset loading
- Threshold computation
- Binary encoding
- Encoded protein
- Encoded ligand

---

## 02_Protein_Segmentation.ipynb

### Purpose

Implements the protein segmentation algorithm.

### Demonstrates

- Ligand-sized segmentation
- Iterative shifting
- Duplicate pattern removal
- Search pattern generation
- Occurrence tracking

---

## 03_Amplitude_Vector.ipynb

### Purpose

Constructs the amplitude vectors used for Grover Search.

### Demonstrates

- Search-space generation
- Basis-state indexing
- Normalized amplitude vectors
- Quantum search state

---

## 04_State_Preparation.ipynb

### Purpose

Verifies arbitrary quantum state preparation.

### Demonstrates

- Amplitude vector initialization
- StatePreparation circuit
- Statevector verification
- Circuit visualization

---

## 05_Oracle.ipynb

### Purpose

Constructs and validates the Grover oracle.

### Demonstrates

- Target state marking
- Phase inversion
- Oracle verification
- Statevector inspection

---

## 06_Diffusion.ipynb

### Purpose

Constructs the custom diffusion operator.

### Demonstrates

- Reflection operator
- Custom unitary generation
- State amplification
- Mathematical verification

---

## 07_Grover_Search.ipynb

### Purpose

Combines state preparation, oracle, and diffusion into the complete Grover Search algorithm.

### Demonstrates

- Complete Grover circuit
- Measurement
- Probability amplification
- Simulator execution
- IBM Quantum execution

---

## 08_Candidate_Evaluation.ipynb

### Purpose

Extracts and filters candidate docking sites obtained from Grover Search.

### Demonstrates

- Candidate extraction
- Duplicate removal
- Probability filtering
- Preparation for Phase 3

---

## 09_Second_Encoding.ipynb

### Purpose

Implements the second encoding stage described in the research paper.

### Demonstrates

- Interaction normalization
- Coefficient computation
- Quantum amplitude generation
- Power-of-two padding
- Final encoded vectors

---

## 10_State_Construction.ipynb

### Purpose

Constructs the quantum states required by the SWAP Test.

### Demonstrates

- Construction of |\(\phi\)\rangle
- Construction of |\(\Psi\)\rangle
- State normalization
- Mathematical verification

---

## 11_SWAP_Test.ipynb

### Purpose

Implements and validates the SWAP Test.

### Demonstrates

- SWAP Test circuit
- Simulator execution
- IBM Quantum execution
- Probability computation
- Euclidean distance estimation
- Candidate ranking

---

# Recommended Execution Order

For users learning the algorithm, execute the notebooks in the following order:

| Order | Notebook |
|------:|----------|
| 1 | 01_First_Encoding.ipynb |
| 2 | 02_Protein_Segmentation.ipynb |
| 3 | 03_Amplitude_Vector.ipynb |
| 4 | 04_State_Preparation.ipynb |
| 5 | 05_Oracle.ipynb |
| 6 | 06_Diffusion.ipynb |
| 7 | 07_Grover_Search.ipynb |
| 8 | 08_Candidate_Evaluation.ipynb |
| 9 | 09_Second_Encoding.ipynb |
| 10 | 10_State_Construction.ipynb |
| 11 | 11_SWAP_Test.ipynb |

---

# Purpose of the Notebook Collection

The notebooks complement the main implementation by providing an interactive environment to

- inspect intermediate data,
- verify mathematical equations,
- visualize quantum circuits,
- debug algorithmic stages,
- reproduce the results presented in the research paper.

Each notebook focuses on one stage of the pipeline, making the implementation easier to understand and extend.

---

# Related Documentation

For more information, refer to

- **Project Overview:** `../README.md`
- **Input Data:** `../data/README.md`
- **Source Code:** `../src/README.md`
- **Generated Outputs:** `../outputs/README.md`