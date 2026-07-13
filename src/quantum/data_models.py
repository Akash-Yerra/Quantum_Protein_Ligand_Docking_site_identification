"""
data_models.py

Dataclasses used by the quantum search module.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.segmentation import SearchPattern

@dataclass
class AmplitudeData:
    """
    Stores the complete description of one
    quantum superposition.

    Attributes
    ----------
    num_qubits
        Number of qubits.

    basis_states
        Binary strings representing encoded windows.

    indices
        Decimal indices of basis states.

    amplitude_vector
        Statevector amplitudes.
    patterns
        list of search patterns
    """
    num_qubits: int
    basis_states: list[str]
    indices: list[int]
    amplitude_vector: np.ndarray
    patterns:list[SearchPattern]

@dataclass
class ProjectData:
    """
    Stores all intermediate classical preprocessing results.

    This object is serialized to disk and loaded by the
    quantum notebooks.
    """
    # version: str = "1.0"
    protein: pd.DataFrame
    ligand: pd.DataFrame
    thresholds: dict
    encoded_protein: pd.DataFrame
    encoded_ligand: pd.DataFrame
    search_iterations: dict
    amplitude_vectors: dict
    interaction_ranges: dict
    
@dataclass
class SearchResult:
    """
    Represents one candidate returned
    by Grover search.
    """
    pattern: SearchPattern
    probability: float
    counts: int
    shift_id: int
    
@dataclass
class GroverSearchOutput:
    shift_id: int
    counts: dict
    threshold: float
    target_probability: float
    matched: bool
    results: list[SearchResult]
    
@dataclass
class StateConstructionResult:
    """
    Stores the quantum states constructed
    for the SWAP Test.
    """
    occurrence: tuple
    probability: float
    phi_state: np.ndarray
    psi_state: np.ndarray
    Z: float

@dataclass
class SecondEncodingResult:
    """
    Stores the second encoded ligand and protein
    quantum states for one candidate.
    """
    occurrence: tuple
    probability: float
    ligand_vector: np.ndarray
    protein_vector: np.ndarray
    
@dataclass
class SwapTestResult:
    """
    Stores the result of one SWAP Test.
    """
    occurrence: tuple
    probability: float
    counts: dict
    p0: float
    distance: float
    Z: float