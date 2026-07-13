"""
grover.py

Builds the complete Grover search circuit.
"""
import math
from qiskit import QuantumCircuit
from src.quantum.state_preparation import StatePreparationBuilder
from src.quantum.oracle import OracleBuilder
from src.quantum.diffusion import DiffusionBuilder
from src.quantum.data_models import AmplitudeData

class GroverBuilder:
    def __init__(self):
        self.state_builder = StatePreparationBuilder()
        self.oracle_builder = OracleBuilder()
        self.diffusion_builder = DiffusionBuilder()
    def build(self,amplitude_data: AmplitudeData,target_state: str,iterations=None) -> QuantumCircuit:
        if iterations is None:
            N = len(amplitude_data.basis_states)
            iterations = max(1, round((math.pi / 4) * math.sqrt(N)))
        Us = self.state_builder.prepare(amplitude_data)
        oracle = self.oracle_builder.build(target_state)
        # diffusion = self.diffusion_builder.build(Us)
        diffusion = self.diffusion_builder.build(amplitude_data)
        
        Us_gate = Us.to_gate(label="State Preparation")
        oracle_gate = oracle.to_gate(label="Oracle")
        diffusion_gate = diffusion.to_gate(label="Diffusion")
        
        qc = QuantumCircuit(amplitude_data.num_qubits,amplitude_data.num_qubits,name="Grover Search")
        
        qc.append(Us_gate,qc.qubits)
        
        for _ in range(iterations):
            qc.append(oracle_gate,qc.qubits)
            qc.append(diffusion_gate,qc.qubits)
        
        qc.measure(qc.qubits,qc.clbits)
        
        return qc
