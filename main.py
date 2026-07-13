"""
main.py

Quantum Protein-Ligand Docking

Pipeline
--------
Phase 1
    • Read input datasets
    • First encoding
    • Protein segmentation
    • Amplitude vector generation

Phase 2
    • Quantum search using Grover's Algorithm

Phase 3
    • Candidate Evaluation (Coming Next)
"""

from prepare_data import prepare_project_data
from src.quantum.quantum_search import QuantumSearch
from src.quantum.candidate_evaluation import CandidateEvaluator
from qiskit_ibm_runtime import QiskitRuntimeService
import pickle

def ligand_to_bitstring(encoded_ligand):
    """
    Convert encoded ligand dataframe
    into a binary string.
    """

    return "".join(
        f"{a}{b}"
        for a, b in encoded_ligand["Encoded"]
    )


def protein_to_bitstring(encoded_protein):
    """
    Convert encoded protein dataframe
    into a binary string.
    """

    return "".join(
        f"{a}{b}"
        for a, b in encoded_protein["Encoded"]
    )

def get_ibm_backend():
    QiskitRuntimeService.save_account(channel="ibm_quantum_platform",
                              instance="your-crn-token",
                              token="your-api-token",overwrite=True)
    #Get the runtimeService to do the operations in cloud.
    service = QiskitRuntimeService()
            
    # Use the least busy backend, or uncomment the loading of a specific backend like "ibm_brisbane".
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
    # backend = service.backend("ibm_kingston")
    print(f"backend using:{backend.name}")
    return backend

def main():

    print("=" * 80)
    print("Quantum Protein-Ligand Docking")
    print("=" * 80)

    # --------------------------------------------------
    # Phase 1
    # --------------------------------------------------

    prepare_project_data()

    with open("outputs/project_data.pkl", "rb") as f:
        project_data = pickle.load(f)

    ligand_bits = ligand_to_bitstring(
        project_data.encoded_ligand
    )

    protein_bits = protein_to_bitstring(
        project_data.encoded_protein
    )

    print()
    print(f"Ligand bits : {ligand_bits}")
    print(f"Protein bits: {protein_bits}")

    # --------------------------------------------------
    # Phase 2
    # --------------------------------------------------

    print()
    print("=" * 80)
    print("Phase 2 : Quantum Search")
    print("=" * 80)
    print()

    quantum_search = QuantumSearch()
    grover_outputs = {}
    iterations = len(project_data.amplitude_vectors)
    backend = get_ibm_backend()
    print(f"Iterations run: {iterations}")

    ##Note: replace hardware = "hardware" and backend = backend to use the real ibm quantum hardware.
    for iteration, amplitude_data in project_data.amplitude_vectors.items():
        output = quantum_search.search(
            shift_id=iteration,
            amplitude_data=amplitude_data,
            target_state=ligand_bits,
            backend= backend,
            hardware="hardware",
            iterations=1,
            shots=1024,
        )
        grover_outputs[iteration] = output
        status = "MATCH" if output.matched else "no match"
        print(
            f"  iter {iteration} "
            f"(shift {iteration-1}): "
            f"{len(output.results)} unique pattern(s), "
            f"P(target)={output.target_probability:.4f} "
            f"[threshold={output.threshold:.4f}] "
            f"-> {status}"
        )
    # print(grover_outputs)
    print()
    print("=" * 80)
    print("Phase 2 Completed Successfully")
    print("=" * 80)

    # --------------------------------------------------
    # Phase 3
    # --------------------------------------------------

    print()
    print("Phase 3 : Candidate Evaluation")

    evaluator = CandidateEvaluator()
    matched_candidates = evaluator.extract_candidates(grover_outputs)

    print("\nMatched Candidates\n")
    # print(matched_candidates)
    len(amplitude_data.patterns) <= 2
    ##Note: replace hardware = "hardware" and backend = backend to use the real ibm quantum hardware.
    results = evaluator.evaluate(
        matched_candidates=matched_candidates,
        project_data=project_data,
        ligand_bits=ligand_bits,
        protein_bits=protein_bits,
        backend= backend,
        hardware="hardware",
        shots=1024,
    )
    best = evaluator.get_best_candidate(results)
    
    print()
    print("=" * 80)
    print("Best Docking Site")
    print("=" * 80)

    start_site = best.occurrence[0]
    end_site = best.occurrence[1]
    
    bit_start = start_site * 2
    bit_end = bit_start + len(ligand_bits)

    matched_bits = protein_bits[bit_start:bit_end]

    print()
    print(f"Protein Bits : {protein_bits}")

    print(" " * 15 + " " * bit_start + "^" * len(ligand_bits))

    print()

    print(f"Matched Bits      : {matched_bits}")
    print(f"Protein Sites     : P{start_site+1} - P{end_site+1}")
    print(f"Interaction Sites : {best.occurrence}")
    print(f"Bit Position      : {bit_start+1} - {bit_end}")
    print(f"Distance          : {best.distance:.6f}")

    print()
    print(
        "Detailed report saved to:\n"
        "outputs/candidate_evaluation/evaluation_report.txt"
    )


if __name__ == "__main__":
    main()