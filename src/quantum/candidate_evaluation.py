"""
candidate_evaluation.py

Phase 3 Controller

Current Responsibilities
------------------------
1. Extract matched candidates from Grover search.
2. Sort candidates by probability.

Future Responsibilities
-----------------------
1. Second Encoding
2. Swap Test
3. Euclidean Distance
4. Candidate Ranking
"""

from src.quantum.data_models import (
    GroverSearchOutput,
    SearchResult,
)
from src.second_encoding import SecondEncoder
from src.quantum.state_construction import StateConstructionBuilder
from src.quantum.swap_test import SwapTestBuilder
import pickle
from pathlib import Path
import json

class CandidateEvaluator:
    """
    Controls the candidate evaluation phase.

    At present, this class only extracts the
    matched protein candidates obtained from
    Grover search.

    The extracted candidates will later be
    passed to the Second Encoding module.
    """

    def __init__(self):
        PROJECT_ROOT = Path(__file__).resolve().parents[2]
        self.output_dir = (PROJECT_ROOT /"outputs" /"candidate_evaluation")
        self.output_dir.mkdir(parents=True,exist_ok=True)

    def extract_candidates(self,grover_outputs: dict[int, GroverSearchOutput],) -> list[SearchResult]:
        """
        Extract all matched candidates from
        Grover search outputs.

        Parameters
        ----------
        grover_outputs
            Dictionary returned by Phase 2.

        Returns
        -------
        list[SearchResult]
            Candidates whose probability is
            greater than or equal to the
            Grover threshold.
        """

        matched_candidates = []

        for output in grover_outputs.values():
            for result in output.results:
                if result.probability >= output.threshold:
                    matched_candidates.append(result)
        matched_candidates.sort(key=lambda candidate: candidate.probability,reverse=True,)
        
        # print(matched_candidates)
        
        unique_candidates = {}

        for candidate in matched_candidates:
            key = (candidate.pattern.binary_window,tuple(candidate.pattern.occurrences))
            if (key not in unique_candidates or candidate.probability > unique_candidates[key].probability):
                unique_candidates[key] = candidate
        matched_candidates = list(unique_candidates.values())
        # print(matched_candidates)
        self._save_candidates(matched_candidates)
        return matched_candidates
    
    
    def _save_candidates(self, matched_candidates):
        """
        Save the matched Grover candidates
        in both text and JSON formats.
        """
        self._save_txt(matched_candidates)
        self._save_json(matched_candidates)
        self._save_pickle(matched_candidates,)
        
    def _save_txt(self, matched_candidates):

        file = self.output_dir / "matched_candidates.txt"
        with open(file, "w") as f:
            for i, candidate in enumerate(matched_candidates, start=1):
                f.write("=" * 70 + "\n")
                f.write(f"Matched Candidate {i}\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Shift          : {candidate.shift_id}\n")
                f.write(f"Probability    : {candidate.probability:.6f}\n")
                f.write(f"Counts         : {candidate.counts}\n")
                f.write(f"Binary Pattern : {candidate.pattern.binary_window}\n\n")
                for occ, values in zip(candidate.pattern.occurrences,candidate.pattern.interaction_values):
                    f.write(f"Occurrence : {occ}\n")
                    f.write("Interaction Values\n")
                    for site, value in zip(range(occ[0], occ[1] + 1),values):
                        f.write(
                            f"    Site {site} : "
                            f"Hydrophobic={value[0]}, "
                            f"HydrogenBond={value[1]}\n"
                        )
                    f.write("\n")
    
    def _save_json(self, matched_candidates):
        file = self.output_dir / "matched_candidates.json"
        data = []
        for candidate in matched_candidates:
            data.append({
                "shift": candidate.shift_id,
                "probability": candidate.probability,
                "counts": candidate.counts,
                "binary_pattern": candidate.pattern.binary_window,
                "occurrences": candidate.pattern.occurrences,
                "interaction_values": candidate.pattern.interaction_values
            })
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    def _save_pickle(self, matched_candidates):
        """
        Save matched candidates for later
        phases and notebooks.
        """
        with open(self.output_dir / "matched_candidates.pkl","wb",) as f:
            pickle.dump(matched_candidates,f,)
            
    
    def evaluate(self,matched_candidates,project_data,ligand_bits,protein_bits,backend=None,hardware="simulator",shots=1024,):
        """
        Complete Phase-3 evaluation.

        Candidate
            ↓
        Second Encoding
            ↓
        State Construction
            ↓
        SWAP Test
            ↓
        Ranking
        """

        ligand_interactions = tuple((row["Hydrophobic"],row["Hydrogen_Bond"],) for _, row in project_data.ligand.iterrows())
        encoder = SecondEncoder(project_data.interaction_ranges)
        builder = StateConstructionBuilder()
        swap_test = SwapTestBuilder()
        results = []
        print()
        print("Evaluating Candidates\n")

        for i, candidate in enumerate(matched_candidates, start=1):
            encoding_result = encoder.build(candidate,ligand_interactions,)
            state_result = builder.build(encoding_result,)
            swap_result = swap_test.run(state_result,backend=backend,hardware=hardware,shots=shots,)
            results.append(swap_result)
            print(
                f"Candidate {i:2d} "
                f"Sites {candidate.pattern.occurrences[0]} "
                f"Distance = {swap_result.distance:.6f}"
            )
        results.sort(key=lambda result: result.distance)
        self.generate_report(ligand_bits,protein_bits,matched_candidates,results,)

        return results
    
    def generate_report(self,ligand_bits,protein_bits,matched_candidates,results,):
        report = self.output_dir / "evaluation_report.txt"

        with open(report, "w") as f:
                f.write("=" * 80 + "\n")
                f.write("Quantum Protein-Ligand Docking Report\n")
                f.write("=" * 80 + "\n\n")

                f.write(f"Ligand Bits : {ligand_bits}\n")
                f.write(f"Protein Bits: {protein_bits}\n\n")
                for i, (candidate, result) in enumerate(zip(matched_candidates, results), start=1):
                    occurrence = result.occurrence
                    start_site = occurrence[0]
                    end_site = occurrence[1]
                    bit_start = start_site * 2
                    bit_end = bit_start + len(ligand_bits)
                    matched_bits = protein_bits[bit_start:bit_end]

                    f.write("-" * 80 + "\n")
                    f.write(f"Candidate {i}\n\n")
                    f.write(f"Protein Sites : P{start_site+1} - P{end_site+1}\n")
                    f.write(f"Occurrence : {occurrence}\n")
                    f.write(f"Matched Bits : {matched_bits}\n")
                    f.write(f"Bit Position : {bit_start} - {bit_end-1}\n")
                    f.write(f"Grover Probability : {candidate.probability:.6f}\n")
                    f.write(f"P(0) : {result.p0:.6f}\n")
                    f.write(f"Distance : {result.distance:.6f}\n\n")
                
                best = results[0]
                start_site = best.occurrence[0]
                end_site = best.occurrence[1]
                bit_start = start_site * 2 +1
                bit_end = bit_start + len(ligand_bits) +1
                matched_bits = protein_bits[bit_start:bit_end]
                f.write("=" * 80 + "\n")
                f.write("BEST DOCKING SITE\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Protein Sites : P{start_site+1} - P{end_site+1}\n")
                f.write(f"Bit Position : {bit_start} - {bit_end-1}\n")
                f.write(f"Matched Bits : {matched_bits}\n")
                f.write(f"Distance : {best.distance:.6f}\n")
    def get_best_candidate(self, results):
        """
        Return the best docking site.
        """
        return min(results,key=lambda result: result.distance,)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                