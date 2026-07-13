"""
oracle.py

Builds the Grover Oracle for any target (ligand)
binary string.

Oracle:
    O = I - 2|t><t|
"""

from qiskit import QuantumCircuit

class OracleBuilder:
    """
    Builds a Grover Oracle for any target state.
    """
    def get_zero_positions(self,target_state: str):
        """
        Returns the positions of all zeros
        in the target state.

        Example
        -------
        "101001"

        Returns
        [1,3,4]
        """
        zero_positions = []

        for i, bit in enumerate(target_state):
            if bit == "0":
                zero_positions.append(i)

        return zero_positions

    def build(self,target_state: str):

        num_qubits = len(target_state)
        qc = QuantumCircuit(num_qubits,name="Oracle")
        zero_positions = self.get_zero_positions(target_state)

        # qc.barrier()
        for position in zero_positions:
            qc.x(num_qubits - 1 - position)

        # qc.barrier()
        target = num_qubits - 1
        # controls = list(range(num_qubits - 1))
        # target = num_qubits - 1
        controls = [q for q in range(num_qubits) if q != target]
        qc.h(target)
        qc.mcx(controls,target)
        qc.h(target)
        # qc.barrier()
        for position in zero_positions:
            qc.x(num_qubits - 1 - position)
        # qc.barrier()
        return qc