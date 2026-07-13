# """
# quantum_search.py

# Runs Grover search for one protein shift.

# Responsibilities
# ----------------
# 1. Build Grover circuit.
# 2. Execute on simulator.
# 3. Convert counts to probabilities.
# 4. Sort candidate interaction sites.
# 5. Return SearchResult objects.
# """

# from qiskit import transpile
# from qiskit_aer import AerSimulator
# from src.quantum.grover import GroverBuilder
# from src.quantum.data_models import (AmplitudeData,SearchResult,)


# class QuantumSearch:
#     """
#     Executes Grover search for one protein shift.
#     """

#     def __init__(self,backend):
#         self.backend = AerSimulator()
#         self.grover_builder = GroverBuilder()

#     def search(self,shift_id: int,amplitude_data: AmplitudeData,target_state: str,iterations: int = 1,shots: int = 1024,):
#         """
#         Parameters
#         ----------
#         amplitude_data : AmplitudeData
#             Search space for one protein shift.

#         target_state : str
#             Encoded ligand bit string.

#         iterations : int
#             Number of Grover iterations.

#         shots : int
#             Number of simulator shots.

#         Returns
#         -------
#         list[SearchResult]
#             Candidate interaction sites sorted
#             by probability (highest first).
#         """

#         # --------------------------------------------------
#         # Build Grover Circuit
#         # --------------------------------------------------

#         grover = self.grover_builder.build(amplitude_data=amplitude_data,target_state=target_state,iterations=iterations,)

#         # --------------------------------------------------
#         # Execute Circuit
#         # --------------------------------------------------

#         compiled = transpile(grover,self.backend,)
#         job = self.backend.run(compiled,shots=shots,)
#         result = job.result()
#         counts = result.get_counts()

        # # --------------------------------------------------
        # # Convert counts to probabilities
        # # --------------------------------------------------

        # probabilities = {state: count / shots for state, count in counts.items()}

        # # --------------------------------------------------
        # # Convert measured states into SearchResult objects
        # # --------------------------------------------------

        # search_results = []
        # for pattern in amplitude_data.patterns:
        #     bitstring = pattern.binary_string
        #     count = counts.get(bitstring, 0)
        #     probability = probabilities.get(bitstring, 0.0)
        #     search_results.append(SearchResult(shift_id=shift_id,pattern=pattern,probability=probability,counts=count,))

        # # --------------------------------------------------
        # # Sort by probability
        # # --------------------------------------------------
        # search_results.sort(key=lambda result: result.probability,reverse=True,)
        
#         return search_results

"""
quantum_search.py

Runs Grover search for one protein shift.

Responsibilities
----------------
1. Build Grover circuit.
2. Execute on simulator or IBM hardware.
3. Save circuits.
4. Save counts and histograms.
5. Compare simulator and hardware results.
6. Return SearchResult objects.
"""

from pathlib import Path
import json

from qiskit import transpile
from qiskit.qpy import dump
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from src.quantum.grover import GroverBuilder
from src.quantum.data_models import (
    AmplitudeData,
    SearchResult,
    GroverSearchOutput
)
from qiskit.transpiler.preset_passmanagers import (
    generate_preset_pass_manager
)
from qiskit_ibm_runtime import Sampler

class QuantumSearch:

    def __init__(self):

        self.grover_builder = GroverBuilder()
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        self.output_dir = PROJECT_ROOT / "outputs"
        self.circuit_dir = self.output_dir / "circuits"
        self.result_dir = self.output_dir / "results"
        self.circuit_dir.mkdir(parents=True,exist_ok=True)
        self.result_dir.mkdir(parents=True,exist_ok=True)
    
    def search(self,shift_id,amplitude_data,target_state,backend,hardware="simulator",iterations=1,shots=1024,):
        grover = self.grover_builder.build(amplitude_data,target_state,iterations,)
        self._save_circuit(shift_id,grover,)
        
        if hardware == "simulator":
            counts = counts = self._run_simulator(grover, shots, shift_id)
        elif hardware == "hardware":
            counts = self._run_hardware(grover,backend,shots,shift_id)
        else:
            raise ValueError("hardware must be either 'simulator' or 'hardware'")

        self._save_results(shift_id,hardware,counts,)
        # --------------------------------------------------
        # Convert counts to probabilities
        # --------------------------------------------------
        probabilities = {state: count / shots for state, count in counts.items()}

        # --------------------------------------------------
        # Convert measured states into SearchResult objects
        # --------------------------------------------------
        search_results = []
        for pattern in amplitude_data.patterns:
            bitstring = pattern.binary_window
            count = counts.get(bitstring, 0)
            probability = probabilities.get(bitstring, 0.0)
            search_results.append(SearchResult(shift_id=shift_id,pattern=pattern,probability=probability,counts=count,))

        # --------------------------------------------------
        # Sort by probability
        # --------------------------------------------------
        search_results.sort(key=lambda result: result.probability,reverse=True,)
        threshold = 1 / len(amplitude_data.patterns)
        
        target_probability = 0.0

        for result in search_results:
            if result.pattern.binary_window == target_state:
                target_probability = result.probability
                break
        
        matched = target_probability >= threshold

        output = GroverSearchOutput(
            shift_id=shift_id,
            counts=counts,
            threshold=threshold,
            results=search_results,
            target_probability=target_probability,
            matched=matched
        )

        self._save_summary(output)

        return output
    
    
    def _run_simulator(self, circuit, shots, shift):

        backend = AerSimulator()

        compiled = transpile(circuit, backend)

        iteration_folder = self.circuit_dir / f"iteration_{shift}"
        simulator_folder = iteration_folder / "simulator"

        simulator_folder.mkdir(parents=True, exist_ok=True)

        figure = compiled.draw("mpl", fold=-1)
        figure.savefig(simulator_folder / "transpiled.png")
        plt.close(figure)
        with open(simulator_folder / "transpiled.qpy", "wb") as f:
            dump(compiled, f)

        info = {
            "backend": "AerSimulator",
            "depth": compiled.depth(),
            "size": compiled.size(),
            "num_qubits": compiled.num_qubits,
            "count_ops": dict(compiled.count_ops())
        }

        with open(simulator_folder / "simulator_info.json", "w") as f:
            json.dump(info, f, indent=4)

        result = backend.run(compiled, shots=shots).result()

        return result.get_counts()
    
    def _run_hardware(self, circuit, backend, shots, shift):
        pm = generate_preset_pass_manager(target=backend.target,optimization_level=3)
        isa = pm.run(circuit)
        iteration_folder = self.circuit_dir / f"iteration_{shift}"
        hardware_folder = iteration_folder / "hardware"
        hardware_folder.mkdir(parents=True, exist_ok=True)

        figure = isa.draw("mpl", fold=-1)
        figure.savefig(hardware_folder / "transpiled.png")
        plt.close(figure)
        with open(hardware_folder / "transpiled.qpy", "wb") as f:
            dump(isa, f)

        hardware_info = {
            "backend": backend.name,
            "optimization_level": 3,
            "depth": isa.depth(),
            "size": isa.size(),
            "num_qubits": isa.num_qubits,
            "count_ops": dict(isa.count_ops())
        }

        with open(hardware_folder / "hardware_info.json", "w") as f:
            json.dump(hardware_info, f, indent=4)

        sampler = Sampler(mode=backend)

        job = sampler.run([isa], shots=shots)

        job_info = {
            "job_id": job.job_id(),
            "backend": backend.name,
            "shots": shots
        }

        with open(hardware_folder / "job_info.json", "w") as f:
            json.dump(job_info, f, indent=4)

        result = job.result()

        return result[0].data.c.get_counts()
    
    def _save_circuit(self, shift, circuit):
        iteration_folder = self.circuit_dir / f"iteration_{shift}"
        original_folder = iteration_folder / "original"
        original_folder.mkdir(parents=True, exist_ok=True)
        figure = circuit.draw("mpl", fold=-1)
        figure.savefig(original_folder / "grover.png")
        plt.close(figure)
        with open(original_folder / "grover.qpy", "wb") as f:
            dump(circuit, f)
        info = {
            "num_qubits": circuit.num_qubits,
            "depth": circuit.depth(),
            "size": circuit.size(),
            "count_ops": dict(circuit.count_ops())
        }
        with open(original_folder / "circuit_info.json", "w") as f:
            json.dump(info, f, indent=4)
    
    def _save_results(self, shift, hardware, counts):
        iteration_folder = self.result_dir / f"iteration_{shift}"
        result_folder = iteration_folder / hardware
        result_folder.mkdir(parents=True, exist_ok=True)
        with open(result_folder / "counts.json", "w") as f:
            json.dump(counts, f, indent=4)
        figure = plot_histogram(counts)
        figure.savefig(result_folder / "histogram.png")
        plt.close(figure)
    
    def _save_summary(self, output):

        iteration_folder = self.result_dir / f"iteration_{output.shift_id}"
        iteration_folder.mkdir(parents=True, exist_ok=True)

        best = output.results[0]

        summary = {
            "shift": output.shift_id,
            "threshold": output.threshold,
            "patterns": len(output.results),
            "best_pattern": best.pattern.binary_window,
            "probability": best.probability,
            "counts": best.counts
        }

        with open(iteration_folder / "summary.json", "w") as f:
            json.dump(summary, f, indent=4)
        
            
    def compare_results(self, shift, simulator_counts, hardware_counts):

        iteration_folder = self.result_dir / f"iteration_{shift}"
        iteration_folder.mkdir(parents=True, exist_ok=True)
        comparison = {
            "simulator_counts": simulator_counts,
            "hardware_counts": hardware_counts,
            "hellinger_fidelity": None
        }
        with open(iteration_folder / "comparison.json", "w") as f:
            json.dump(comparison, f, indent=4)
        figure = plot_histogram(
            [simulator_counts, hardware_counts],
            legend=["Simulator", "Hardware"]
        )
        figure.savefig(iteration_folder / "comparison.png")
        plt.close(figure)

    