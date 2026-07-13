"""
second_encoding.py

Implements the Second Encoding stage described in the paper.

Converts the interaction values of a ligand or
protein docking site into quantum amplitude vectors
used for the SWAP Test.

Encoding Pipeline
-----------------
(Hydrophobic, Hydrogen Bond)
        │
        ▼
Equations (16)-(19)
        │
        ▼
a|0> + b|1>
c|0> + d|1>
        │
        ▼
Tensor Product
        │
        ▼
ac|00> + ad|01> + bc|10> + bd|11>
        │
        ▼
Concatenate all interaction-site vectors
"""

import numpy as np
import pandas as pd
from src.quantum.data_models import SecondEncodingResult

class SecondEncoder:
    def __init__(self, interaction_ranges):
        """
        Parameters
        ----------
        interaction_ranges

        The global minimum and maximum interaction
        values are computed once and reused for
        every encoding.
        """
        self.h_min = interaction_ranges["h_min"]
        self.h_max = interaction_ranges["h_max"]

        self.hb_min = interaction_ranges["hb_min"]
        self.hb_max = interaction_ranges["hb_max"]

    def build(self,candidate,ligand_interactions,):
        """
        Build the second encoding result for one
        matched protein candidate.

        Parameters
        ----------
        candidate : SearchResult
        ligand_interactions : tuple
        Returns
        -------
        SecondEncodingResult
        """

        ligand_vector = self.encode(ligand_interactions)
        protein_vector = self.encode(candidate.pattern.interaction_values[0])

        return SecondEncodingResult(
            occurrence=candidate.pattern.occurrences[0],
            probability=candidate.probability,
            ligand_vector=ligand_vector,
            protein_vector=protein_vector,
        )


    # -----------------------------------------------------
    # Equation (16)-(19)
    # -----------------------------------------------------

    def _compute_coefficients(self,hydrophobic,hydrogen_bond,):
        """
        Compute
            a,b,c,d
        from Equations (16)-(19).
        """

        # -----------------------------
        # Hydrophobic
        # -----------------------------
        h_denominator = np.sqrt((self.h_max - hydrophobic) ** 2 + (hydrophobic - self.h_min) ** 2)
        a = ((self.h_max - hydrophobic)/ h_denominator)
        b = ((hydrophobic - self.h_min)/ h_denominator)

        # -----------------------------
        # Hydrogen Bond
        # -----------------------------

        hb_denominator = np.sqrt((self.hb_max - hydrogen_bond) ** 2 + (hydrogen_bond - self.hb_min) ** 2)
        c = ((self.hb_max - hydrogen_bond)/ hb_denominator)
        d = ((hydrogen_bond - self.hb_min)/ hb_denominator)

        return a, b, c, d

    # -----------------------------------------------------
    # Equation (20)
    # -----------------------------------------------------

    def _encode_interaction(self,interaction,):
        """
        Encode one interaction site.

        Parameters
        ----------
        interaction
            (Hydrophobic, Hydrogen_Bond)

        Returns
        -------
        np.ndarray
        [ac, ad, bc, bd]
        """

        hydrophobic, hydrogen_bond = interaction
        a, b, c, d = self._compute_coefficients(hydrophobic,hydrogen_bond,)

        return np.array([a * c, a * d,b * c,b * d,],dtype=float,)

    # -----------------------------------------------------
    # Complete Candidate Encoding
    # -----------------------------------------------------

    def encode(self,interaction_values,):
        """
        Encode a complete ligand or
        protein docking site.

        Parameters
        ----------
        interaction_values

            Example

            (
                (2.69,0.31),
                (0.12,-0.34)
            )

        Returns
        -------
        np.ndarray

        Final amplitude vector.
        """

        amplitude_vector = []
        for interaction in interaction_values:
            amplitude_vector.extend(self._encode_interaction(interaction))

        amplitude_vector = np.array(amplitude_vector,dtype=float,)

        # Numerical normalization

        amplitude_vector /= np.linalg.norm(amplitude_vector)
        
        #Pad the left over states amplitudes with zeros.
        amplitude_vector = self._pad_to_power_of_two(amplitude_vector)
        #normalize again.
        amplitude_vector /= np.linalg.norm(amplitude_vector)
        return amplitude_vector

    
    def _pad_to_power_of_two(self, vector):
        """
        Pad an amplitude vector with zeros so that its
        length is the next power of two.
        """
        length = len(vector)
        target = 1 << (length - 1).bit_length()
        if target == length:
            return vector
        padded = np.zeros(target, dtype=float)
        padded[:length] = vector
        return padded