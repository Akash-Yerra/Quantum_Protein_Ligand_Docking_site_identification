"""
swap_test.py

Builds the SWAP Test circuit described in the paper.

Input
-----
StateConstructionResult

Output
------
QuantumCircuit

The circuit prepares

    |φ⟩
    |Ψ⟩

and performs the SWAP Test between

    ancilla(|Ψ⟩)

and

    |φ⟩
"""

import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

from src.quantum.data_models import (
    StateConstructionResult,SwapTestResult
)
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

from qiskit import transpile
from qiskit.qpy import dump
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

from qiskit.transpiler.preset_passmanagers import (
    generate_preset_pass_manager,
)
from qiskit_ibm_runtime import Sampler


class SwapTestBuilder:
    """
    Builds the SWAP Test circuit.
    """
    def __init__(self):
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        self.output_dir = PROJECT_ROOT / "outputs"
        self.swap_dir = self.output_dir / "swap_test"
        self.swap_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def build(self,state_result: StateConstructionResult,):
        """
        Build the SWAP Test circuit.

        Parameters
        ----------
        state_result : StateConstructionResult

        Returns
        -------
        QuantumCircuit
        """

        phi = state_result.phi_state
        psi = state_result.psi_state

        # ---------------------------------------
        # Number of data qubits
        #
        # len(psi)=2^(n+1)
        #
        # therefore
        #
        # n = log2(len(psi)) - 1
        # ---------------------------------------

        n = int(np.log2(len(psi))) - 1

        # ---------------------------------------
        # Register layout
        #
        # q0      : SWAP control
        #
        # q1      : |φ⟩
        #
        # q2...   : ancilla of |Ψ⟩
        #
        # last    : data register
        # ---------------------------------------

        ctrl = 0
        anc1 = 2
        anc2 = 1
        data = list(range(3,3 + n,))
        

        qc = QuantumCircuit(n + 3,1,name="Swap_Test",)

        # ---------------------------------------
        # Prepare |φ⟩
        # ---------------------------------------
        qc.append(StatePreparation(phi),[anc2],)
        
       # ---------------------------------------
        # Prepare |Ψ⟩
        #
        # IMPORTANT:
        #
        # StatePreparation expects
        # least-significant qubit first.
        #
        # Therefore use
        #
        # data + [anc1]
        # ---------------------------------------
        qc.append(StatePreparation(psi),data+[anc1],)
        

        # ---------------------------------------
        # SWAP Test
        # ---------------------------------------
        qc.h(ctrl)
        qc.cswap(ctrl, anc1, anc2,)
        qc.h(ctrl)
        qc.measure(ctrl,0,)
        return qc
    
    def _run_simulator(self,circuit,shots,):
        backend = AerSimulator()
        compiled = transpile(circuit,backend,)
        result = backend.run(compiled,shots=shots,).result()
        return (result.get_counts(),compiled)
    
    def _run_hardware(self,circuit,backend,shots,):
        pm = generate_preset_pass_manager(target=backend.target,optimization_level=3,)
        isa = pm.run(circuit)
        sampler = Sampler(mode=backend,)

        job = sampler.run([isa],shots=shots,)
        result = job.result()
        return (result[0].data.c.get_counts(),isa,job)
    
    def _compute_probability(self,counts,shots,):
        return counts.get("0", 0) / shots
    
    def _compute_distance(self,p0,Z,):
        value = max(0.0,4 * Z * (p0 - 0.5),)
        return float(np.sqrt(value))
    
    def _save_circuit(self,occurrence,circuit,executed=False,hardware="simulator",backend=None,job=None):
        folder = (self.swap_dir / f"{occurrence[0]}_{occurrence[1]}")
        if executed:
            folder = (self.swap_dir / f"{occurrence[0]}_{occurrence[1]}" / hardware)
        folder.mkdir(parents=True,exist_ok=True,)
        figure = circuit.draw("mpl",fold=-1,)
        if executed:
            figure.savefig(folder / "transpiled.png")
            plt.close(figure)
            backend_name = "simulator" if backend==None else backend.name
            if backend == None:
                backend_name = "simulator"
            else:
                backend_name = backend.name
                job_info = {
                    "job_id": job.job_id(),
                    "backend": backend.name,
                }
                with open(folder / "job_info.json", "w") as f:
                    json.dump(job_info, f, indent=4)
            info = {
                "backend" : backend_name,
                "qubits": circuit.num_qubits,
                "depth": circuit.depth(),
                "size": circuit.size(),
                "operations": dict(circuit.count_ops()),
            }
        else:
            figure.savefig(folder / "swap_test.png")
            plt.close(figure)
            with open(folder / "swap_test.qpy", "wb",) as f:
                dump(circuit,f,)
            info = {
                "qubits": circuit.num_qubits,
                "depth": circuit.depth(),
                "size": circuit.size(),
                "operations": dict(circuit.count_ops()),
            }

        with open(folder / "circuit_info.json","w",) as f:
            json.dump(info,f,indent=4,)
    
    def _save_results(self,occurrence,hardware,counts,):

        folder = (self.swap_dir/ f"{occurrence[0]}_{occurrence[1]}" / hardware)
        folder.mkdir(parents=True,exist_ok=True,)

        with open(folder / "counts.json","w",) as f:
            json.dump(counts,f,indent=4,)

        figure = plot_histogram(counts)
        figure.savefig(folder / "histogram.png")
        plt.close(figure)
        
    def run(self,state_result,backend=None,hardware="simulator",shots=1024,):
        circuit = self.build(state_result,)
        self._save_circuit(state_result.occurrence,circuit,)
        if hardware == "simulator":
            result = self._run_simulator(circuit,shots,)
            counts = result[0]
            qc = result[1]
            job = None
        elif hardware == "hardware":
            result = self._run_hardware(circuit,backend,shots)
            counts = result[0]
            qc = result[1]
            job = result[2]
        else:
            raise ValueError("hardware must be either 'simulator' or 'hardware'")
        self._save_circuit(state_result.occurrence,qc,executed=True,hardware=hardware,backend=backend,job=job)
        self._save_results(state_result.occurrence,hardware,counts,)
        p0 = self._compute_probability(counts,shots,)
        distance = self._compute_distance(p0,state_result.Z,)
        return SwapTestResult(
            occurrence=state_result.occurrence,
            probability=state_result.probability,
            counts=counts,
            p0=p0,
            distance=distance,
            Z=state_result.Z,
        )