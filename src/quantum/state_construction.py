"""
state_construction.py

Constructs the quantum states |φ⟩ and |Ψ⟩ used
for the SWAP Test.

Input
-----
Second encoded ligand and protein amplitude vectors.

Output
------
|φ⟩
|Ψ⟩

according to Equations (21)-(23) of the paper.
"""

import numpy as np

from src.quantum.data_models import (
    SecondEncodingResult,
    StateConstructionResult,
)


class StateConstructionBuilder:
    """
    Builds the |φ⟩ and |Ψ⟩ quantum states
    required for the SWAP Test.
    """

    # --------------------------------------------------
    # Vector Norms
    # --------------------------------------------------

    def _compute_norms(self,ligand_vector,protein_vector,):
        """
        Compute ||A|| and ||B||.
        """
        norm_A = np.linalg.norm(ligand_vector)
        norm_B = np.linalg.norm(protein_vector)
        return norm_A, norm_B

    # --------------------------------------------------
    # Equation (22)
    # --------------------------------------------------

    def _compute_Z(self,norm_A,norm_B,):
        """
        Compute
            Z = ||A||² + ||B||²
        """
        return norm_A**2 + norm_B**2

    # --------------------------------------------------
    # Tensor Product
    # --------------------------------------------------

    def _tensor_zero(self,vector,):
        """
        |0> ⊗ vector
        """
        return np.concatenate([vector,np.zeros_like(vector),])

    def _tensor_one(self,vector,):
        """
        |1> ⊗ vector
        """
        return np.concatenate([np.zeros_like(vector),vector,])

    # --------------------------------------------------
    # Equation (21)
    # --------------------------------------------------

    def _build_phi(self, norm_A, norm_B, Z):
        """
        Construct
            |φ⟩ = ( ||A|| |0⟩ -||B|| |1⟩ ) / √Z

        Equation (21)
        """
        phi = np.array([ norm_A,-norm_B,], dtype=float,)
        phi /= np.sqrt(Z)

        return phi

    # --------------------------------------------------
    # Equation (23)
    # --------------------------------------------------

    def _build_psi(self,ligand_vector,protein_vector,):
        """
        Construct
        |Ψ⟩ =
        ( |0>|A⟩
        +
          |1>|B⟩ )
        / √2
        """
        psi = (self._tensor_zero(ligand_vector) + self._tensor_one(protein_vector)) / np.sqrt(2)

        return psi

    # --------------------------------------------------
    # Main Builder
    # --------------------------------------------------

    def build(self, encoding_result: SecondEncodingResult,):
        """
        Construct |φ⟩ and |Ψ⟩.
        """
        ligand_vector = encoding_result.ligand_vector
        protein_vector = encoding_result.protein_vector
        norm_A, norm_B = self._compute_norms(ligand_vector,protein_vector,)

        Z = self._compute_Z(norm_A,norm_B,)

        phi_state = self._build_phi(norm_A,norm_B, Z,)
        psi_state = self._build_psi(ligand_vector,protein_vector,)

        return StateConstructionResult(
            occurrence=encoding_result.occurrence,
            probability=encoding_result.probability,
            phi_state=phi_state,
            psi_state=psi_state,
            Z=Z,
        )