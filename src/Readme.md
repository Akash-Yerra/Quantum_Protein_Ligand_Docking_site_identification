# Source Code Documentation

The **src** directory contains the complete implementation of the hybrid quantum–classical protein–ligand docking framework.

The implementation follows a modular object-oriented architecture, where each module corresponds to a specific stage of the algorithm proposed in the research paper.

---

# Directory Structure

```text
src/

├── encoding.py
├── segmentation.py
├── second_encoding.py
│
├── quantum/
│   ├── amplitude_vector.py
│   ├── candidate_evaluation.py
│   ├── data_models.py
│   ├── diffusion.py
│   ├── grover.py
│   ├── oracle.py
│   ├── quantum_search.py
│   ├── state_construction.py
│   ├── state_preparation.py
│   └── swap_test.py
```

---

# Source Code Workflow

The source code follows the complete workflow shown below.

```text
Interaction Data
        │
        ▼
encoding.py
        │
        ▼
segmentation.py
        │
        ▼
amplitude_vector.py
        │
        ▼
state_preparation.py
        │
        ▼
oracle.py
        │
        ▼
diffusion.py
        │
        ▼
grover.py
        │
        ▼
quantum_search.py
        │
        ▼
candidate_evaluation.py
        │
        ▼
second_encoding.py
        │
        ▼
state_construction.py
        │
        ▼
swap_test.py
        │
        ▼
Best Docking Site
```

---

# Classical Modules

These modules perform all preprocessing before the quantum algorithms are executed.

---

## encoding.py

### Purpose

Implements the **First Encoding** stage of the algorithm.

### Responsibilities

- Compute binary representation of interaction sites
- Encode Hydrophobic interaction
- Encode Hydrogen Bond interaction
- Produce encoded protein and ligand datasets

### Input

```
Protein DataFrame

Ligand DataFrame
```

### Output

```
Encoded Protein

Encoded Ligand
```

---

## segmentation.py

### Purpose

Implements the **Protein Segmentation and Shift Algorithm**.

### Responsibilities

- Generate ligand-sized windows
- Perform iterative shifting
- Remove duplicate patterns within each iteration
- Store all occurrences of identical patterns
- Generate search patterns for Grover Search

### Input

```
Encoded Protein
```

### Output

```
SearchPattern objects
```

---

## second_encoding.py

### Purpose

Implements the **Second Encoding** stage.

Unlike the first encoding, this stage converts the original interaction values into quantum amplitudes.

### Responsibilities

- Compute coefficients using the equations in the paper
- Normalize interaction vectors
- Construct amplitude vectors
- Pad vectors to the nearest power of two

### Input

```
Interaction Values
```

### Output

```
Quantum Amplitude Vector
```

---

# Quantum Modules

These modules implement the quantum algorithms.

---

## amplitude_vector.py

### Purpose

Construct the amplitude vector representing the search space.

### Responsibilities

- Encode unique search patterns
- Compute basis-state indices
- Generate normalized amplitude vectors
- Store amplitude information

### Output

```
AmplitudeData
```

---

## state_preparation.py

### Purpose

Construct the quantum superposition used during Grover Search.

### Responsibilities

- Prepare arbitrary quantum states
- Build StatePreparation circuits
- Initialize the search space

---

## oracle.py

### Purpose

Construct the Grover Oracle.

### Responsibilities

- Mark the ligand bit string
- Apply phase inversion
- Generate reusable oracle circuit

---

## diffusion.py

### Purpose

Construct the custom diffusion operator.

Instead of the standard Grover diffusion operator, the implementation reflects about the prepared search state.

### Responsibilities

- Build

```
2|s><s|−I
```

- Generate custom unitary operator

---

## grover.py

### Purpose

Assemble the complete Grover Search circuit.

### Responsibilities

- State Preparation
- Oracle
- Diffusion
- Multiple iterations
- Measurement

---

## quantum_search.py

### Purpose

Execute the Grover Search.

### Responsibilities

- Execute simulator
- Execute IBM Quantum hardware
- Save circuits
- Save transpiled circuits
- Store measurement counts
- Generate histograms
- Compute target probabilities
- Produce search results

---

## state_construction.py

### Purpose

Construct the quantum states required for the SWAP Test.

### Responsibilities

Build

```
|φ⟩
```

and

```
|Ψ⟩
```

according to the equations presented in the paper.

---

## swap_test.py

### Purpose

Evaluate candidate docking sites using the quantum SWAP Test.

### Responsibilities

- Construct SWAP Test circuit
- Execute simulator
- Execute IBM hardware
- Compute

```
P(0)
```

- Estimate Euclidean distance
- Store evaluation results

---

## candidate_evaluation.py

### Purpose

Evaluate all candidate docking sites returned by Grover Search.

### Responsibilities

- Extract matched candidates
- Remove duplicate occurrences
- Execute Second Encoding
- Construct quantum states
- Perform SWAP Test
- Rank candidates
- Generate docking report
- Select the best docking site

---

## data_models.py

### Purpose

Contains all shared data classes used throughout the project.

### Examples

- SearchPattern
- SearchResult
- AmplitudeData
- GroverSearchOutput
- SecondEncodingResult
- StateConstructionResult
- SwapTestResult
- ProjectData

Using dataclasses keeps the implementation modular and type-safe.

---

# Design Philosophy

The project follows the **Single Responsibility Principle (SRP)**.

Each module performs one well-defined task and communicates with other modules only through structured data classes.

This modular design provides

- Better readability
- Easier debugging
- Independent testing
- Reusable components
- Simple future extensions

---

# Data Flow

The implementation processes information in the following order.

```text
Protein CSV
        │
Ligand CSV
        │
        ▼
First Encoding
        │
        ▼
Protein Segmentation
        │
        ▼
Amplitude Vector
        │
        ▼
Grover Search
        │
        ▼
Candidate Extraction
        │
        ▼
Second Encoding
        │
        ▼
State Construction
        │
        ▼
SWAP Test
        │
        ▼
Distance Evaluation
        │
        ▼
Best Docking Site
```

---

# Extending the Project

Researchers can easily extend the implementation by adding modules for

- Additional interaction descriptors
- Alternative encoding strategies
- New quantum search algorithms
- Error mitigation techniques
- Quantum machine learning models
- Advanced similarity metrics
- Integration with molecular docking software

The modular architecture ensures that new components can be added with minimal changes to the existing codebase.

---

# Related Documentation

For more information, refer to:

- **Project Overview:** `../README.md`
- **Input Data:** `../data/README.md`
- **Generated Outputs:** `../outputs/README.md`
- **Example Notebooks:** `../notebooks/README.md`