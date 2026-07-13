"""
prepare_data.py

Runs the complete classical preprocessing pipeline and
stores all intermediate data required for the quantum
algorithm.

Run this script only when the input CSV files change.
"""

import os
import pickle

from src.encoding import (
    load_interaction_data,
    validate_dataset,
    compute_thresholds,
    encode_dataset
)

from src.segmentation import ProteinSegmenter
from src.quantum.amplitude_vector import  AmplitudeVectorBuilder
from src.quantum.data_models import ProjectData

from pathlib import Path


def save_segmentations(search_iterations, output_file):
    """
    Save the segmented bitstrings for every shift.

    Parameters
    ----------
    search_iterations : dict[int, list[SearchPattern]]

    output_file : str | Path
    """
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        for iteration, patterns in search_iterations.items():
            bitstrings = []
            for pattern in patterns:
                # repeat once for every occurrence
                bitstrings.extend([pattern.binary_window] * len(pattern.occurrences))
            f.write(
                f"Set-{iteration} : "
                + ", ".join(bitstrings)
                + "\n"
            )

def prepare_project_data():
    """
    Run the complete classical preprocessing pipeline.
    """
    print("=" * 70)
    print("Reading Input Files")
    print("=" * 70)

    protein = load_interaction_data("data/protein1.csv")
    ligand = load_interaction_data("data/ligand1.csv")

    validate_dataset(protein)
    validate_dataset(ligand)

    thresholds = compute_thresholds(protein)
    encoded_protein = encode_dataset(protein,thresholds)
    encoded_ligand = encode_dataset(ligand,thresholds)

    segmenter = ProteinSegmenter(encoded_protein,len(encoded_ligand))
    
    search_iterations = {}
    iteration = 1

    while True:
        patterns = segmenter.next_iteration()
        if patterns is None:
            break
        search_iterations[iteration] = patterns
        iteration += 1
    PROJECT_ROOT = Path(__file__).resolve().parents[0]
    save_segmentations(
        search_iterations,
        PROJECT_ROOT / "outputs" / "preprocessing" / "segmentations.txt"
    )
    
    amplitude_vectors = {}

    for iteration, patterns in search_iterations.items():
        builder = AmplitudeVectorBuilder(patterns)
        amplitude_vectors[iteration] = builder.build()
    interaction_ranges = {
        "h_min": min(protein["Hydrophobic"].min(),ligand["Hydrophobic"].min(),),
        "h_max": max(protein["Hydrophobic"].max(),ligand["Hydrophobic"].max(),),
        "hb_min": min(protein["Hydrogen_Bond"].min(),ligand["Hydrogen_Bond"].min(),),
        "hb_max": max(protein["Hydrogen_Bond"].max(),ligand["Hydrogen_Bond"].max(),),
    }
    project_data = ProjectData(
        protein=protein,
        ligand=ligand,
        thresholds=thresholds,
        interaction_ranges = interaction_ranges,
        encoded_protein=encoded_protein,
        encoded_ligand=encoded_ligand,
        search_iterations=search_iterations,
        amplitude_vectors=amplitude_vectors
    )

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/project_data.pkl","wb") as f:
        pickle.dump(project_data,f)
        
    print("\n")
    print("=" * 70)
    print("Preprocessing Completed Successfully")
    print("=" * 70)

    print(f"Protein Sites        : {len(protein)}")
    print(f"Ligand Sites         : {len(ligand)}")
    print(f"Search Iterations    : {len(search_iterations)}")
    print(f"Amplitude Vectors    : {len(amplitude_vectors)}")

    print("\nSaved to")

    print("outputs/project_data.pkl")
    
    # print(amplitude_vectors)
    