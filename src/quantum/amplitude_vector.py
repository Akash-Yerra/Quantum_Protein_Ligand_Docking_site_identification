"""
amplitude_vector.py

Builds the amplitude vector corresponding to one
protein search iteration.

"""

import numpy as np
from math import sqrt
from src.quantum.data_models import AmplitudeData

class AmplitudeVectorBuilder:
    """
    Builds the amplitude vector for one search iteration.

    Example
    -------
    Patterns
        101001
        000110
    gives:
    |ψ> = (|101001> + |000110>) / √2
    """
    def __init__(self, patterns):
        self.patterns = patterns
        # print(patterns)

    def build(self):
        """
        Build the amplitude vector.

        Returns
        -------
        dict

        {
            "num_qubits": int,
            "basis_states": list,
            "indices": list,
            "amplitude_vector": np.ndarray
        }
        """

        if len(self.patterns) == 0:
            raise ValueError("Pattern list is empty.")

        basis_states = [pattern.binary_window for pattern in self.patterns]
        # basis_states = ["00"]
        num_qubits = len(basis_states[0])
        dimension = 2**num_qubits
        amplitude_vector = np.zeros(dimension,dtype=float)
        # print(amplitude_vector)
        indices = []

        for state in basis_states:
            decimal = int(state, 2)
            indices.append(decimal)

        amplitude = 1 / sqrt(len(indices))

        for idx in indices:
            amplitude_vector[idx] = amplitude

        return AmplitudeData(
            num_qubits=num_qubits,
            basis_states=basis_states,
            indices=indices,
            amplitude_vector=amplitude_vector,
            patterns=self.patterns
        )
        
    
    
    