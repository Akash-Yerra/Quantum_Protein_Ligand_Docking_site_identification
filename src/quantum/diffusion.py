# # """
# # standard_diffusion.py

# # Builds the Grover diffusion operator.

# #     D = Uₛ D₀ Uₛ†
# # """

# from qiskit import QuantumCircuit
# from src.quantum.oracle import OracleBuilder


# class DiffusionBuilder:
#     def __init__(self):
#         self.oracle_builder = OracleBuilder()

#     def build(self,state_preparation: QuantumCircuit) -> QuantumCircuit:
#         """
#         Builds the Grover diffusion operator
#             D = Uₛ D₀ Uₛ†
#         """
#         num_qubits = state_preparation.num_qubits
#         diffusion = QuantumCircuit(num_qubits,name="Diffusion")

#         zero_state = "0" * num_qubits
#         diffusion_about_zero = self.oracle_builder.build(zero_state)

#         diffusion.h(range(num_qubits))
#         # diffusion.compose(state_preparation.inverse(),inplace=True)
#         # diffusion.barrier()
#         diffusion.compose(diffusion_about_zero,inplace=True)
#         # diffusion.barrier()
#         # diffusion.compose(state_preparation,inplace=True)
#         diffusion.h(range(num_qubits))
        
#         return diffusion



"""
diffusion.py

Builds the Grover diffusion operator

    D = 2|s><s| - I

where |s> is the protein search state
obtained from the amplitude vector.
"""

import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from src.quantum.data_models import AmplitudeData


class DiffusionBuilder:
    """
    Builds the Grover diffusion operator

        D = 2|s><s| - I
    """

    def __init__(self):
        pass

    def build(self,amplitude_data: AmplitudeData) -> QuantumCircuit:
        """
        Parameters
        ----------
        amplitude_data : AmplitudeData

        Returns
        -------
        QuantumCircuit
            Diffusion operator circuit.
        """

        # |s>
        s = amplitude_data.amplitude_vector.astype(complex)
        
        # Dimension = 2^n
        dimension = len(s)

        # D = -H*(I-2|0><0|)*H
        
        # D = 2|s><s| - I
        diffusion_matrix = (2 * np.outer(s, s.conjugate())- np.eye(dimension, dtype=complex))
        diffusion_gate = UnitaryGate(diffusion_matrix,label="Diffusion")
        qc = QuantumCircuit(amplitude_data.num_qubits,name="Diffusion")
        qc.append(diffusion_gate,qc.qubits)

        return qc