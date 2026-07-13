"""
segmentation.py

Protein Segmentation and Shift

Implements the iterative segmentation algorithm
described in the paper.
"""

from dataclasses import dataclass, field
import pandas as pd
from pathlib import Path

@dataclass
class SearchPattern:
    """
    Represents one unique interaction pattern.

    Example
    -------
    encoded_window
        ((1,1),)
    occurrences
        [(0,0),(1,1),(3,3)]
    interaction_values
        [((1.95,1.42),),((1.77,0.42),),((2.28,0.13),)        ]
    """
    encoded_window: tuple
    occurrences: list = field(default_factory=list)
    interaction_values: list = field(default_factory=list)
    
    @property
    def binary_window(self):
        """
        Returns the encoded window as a binary string.
        Example:
        ((1,0),(1,0),(0,1))
            ↓
        "101001"
        """
        return "".join(str(bit) for pair in self.encoded_window for bit in pair)



class ProteinSegmenter:

    def __init__(self,encoded_df: pd.DataFrame,ligand_size: int):
        self.df = encoded_df
        self.encoded_sites = encoded_df["Encoded"].tolist()
        self.length = len(self.encoded_sites)
        self.ligand_size = ligand_size
        self.current_shift = 0
        # Patterns already searched
        self.visited = set()
        # Save every iteration
        self.iterations = []
    
    # def next_iteration(self):
    #     """
    #     Generate the next protein segmentation.
    #     Returns list[Segment]
    #     -------
    #     Returns None when
    #     no new segments exist.
    #     """

    #     segments = []
    #     i = self.current_shift

    #     while i + self.ligand_size <= self.length:
    #         window = tuple(self.encoded_sites[i:i+self.ligand_size])
    #         if window not in self.visited:
    #             segment = Segment(start=i,end=i+self.ligand_size-1,window=window)
    #             segments.append(segment)
    #             self.visited.add(window)
    #         i += self.ligand_size
        
    #     if len(segments) == 0:
    #         return None
        
    #     self.iterations.append(segments)
    #     self.current_shift += 1
    #     return segments
    
    # def print_iteration(self,iteration_number,segments):
    #     print()
    #     print("="*60)
    #     print(f"Iteration {iteration_number}")
    #     print("="*60)

    #     for s in segments:
    #         print(f"Sites {s.start} - {s.end} : {list(s.window)}")
    
    def next_iteration(self):
        """
        Generate one search iteration.
        Returns
        -------
        list[SearchPattern]

        None if no new search patterns exist.
        """
        # self.visited = set()
        pattern_dict = {}
        i = self.current_shift
        while i + self.ligand_size <= self.length:
            encoded_window = tuple(self.encoded_sites[i:i+self.ligand_size])

            # Skip patterns already searched
            # if encoded_window in self.visited:
            #     i += self.ligand_size
            #     continue

            # Original interaction values
            interaction_window = []
            for j in range(i, i+self.ligand_size):
                row = self.df.iloc[j]
                interaction_window.append((row["Hydrophobic"],row["Hydrogen_Bond"]))

            interaction_window = tuple(interaction_window)

            # First occurrence of this pattern
            if encoded_window not in pattern_dict:
                pattern_dict[encoded_window] = SearchPattern(encoded_window=encoded_window)
            pattern = pattern_dict[encoded_window]
            pattern.occurrences.append((i, i+self.ligand_size-1))
            pattern.interaction_values.append(interaction_window)

            i += self.ligand_size            
        patterns = list(pattern_dict.values())

        if len(patterns) == 0:
            return None
        self.iterations.append(patterns)
        self.current_shift += 1
        return patterns
    
    def print_iteration(self,iteration_number,patterns):
        print()
        print("=" * 70)
        print(f"Iteration {iteration_number}")
        print("=" * 70)

        for p in patterns:
            print()
            print("Encoded Window :",p.encoded_window)
            print("Occurrences   :",p.occurrences)
            print("Interaction Values:")

            for value in p.interaction_values:
                print("   ", value)
    
    @property
    def binary_string(self):
        """
        Example
        ((1,0),(1,0),(0,1))
        →
        "101001"
        """
        return "".join(f"{a}{b}" for a, b in self.encoded_window)