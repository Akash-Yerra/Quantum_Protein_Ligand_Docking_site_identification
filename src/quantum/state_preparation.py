"""
state_preparation.py

Creates the initial quantum state
used in the modified Grover search.
"""

from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from src.quantum.data_models import AmplitudeData


class StatePreparationBuilder:
    """
    Creates the quantum circuit that prepares
    the protein search state.
    """

    def prepare(self,amplitude_data: AmplitudeData) -> QuantumCircuit:
        qc = QuantumCircuit(amplitude_data.num_qubits,name="State Preparation")
        state_preparation = StatePreparation(amplitude_data.amplitude_vector)
        qc.append(state_preparation,qc.qubits)

        return qc