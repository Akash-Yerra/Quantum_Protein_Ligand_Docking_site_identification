"""
encoding.py

Phase 1: Classical preprocessing.

This module is responsible for

1. Reading protein and ligand interaction data
2. Validating the dataset
3. Computing interaction thresholds
4. Performing the first encoding

Author: Akash Yerra
"""

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# Required Columns
# ------------------------------------------------------------

REQUIRED_COLUMNS = [
    "Site_ID",
    "Hydrophobic",
    "Hydrogen_Bond"
]


# ------------------------------------------------------------
# Read CSV File
# ------------------------------------------------------------

def load_interaction_data(filepath: str) -> pd.DataFrame:
    """
    Load interaction data from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing interaction data.
    """

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(
            f"File not found: {filepath}"
        )

    df = pd.read_csv(filepath)

    return df


# ------------------------------------------------------------
# Validate Dataset
# ------------------------------------------------------------

def validate_dataset(df: pd.DataFrame) -> None:
    """
    Validate the interaction dataset.

    Checks
    ------
    1. Required columns exist
    2. No missing values
    3. Site IDs are unique
    4. Interaction values are numeric

    Raises
    ------
    ValueError
        If validation fails.
    """

    # Check columns
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Missing values
    if df.isnull().sum().sum() != 0:
        raise ValueError(
            "Dataset contains missing values."
        )

    # Duplicate Site IDs
    if df["Site_ID"].duplicated().any():
        raise ValueError(
            "Duplicate Site_ID values detected."
        )

    # Numeric values
    for col in ["Hydrophobic", "Hydrogen_Bond"]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(
                f"{col} must contain numeric values."
            )

    print("Dataset validation successful.")
    

# ------------------------------------------------------------
# Compute Interaction Thresholds
# ------------------------------------------------------------

def compute_thresholds(df: pd.DataFrame) -> dict:
    """
    Compute threshold values for the first encoding.

    Threshold = (minimum + maximum) / 2

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    dict

    Example

    {
        "hydrophobic": 1.82,
        "hydrogen_bond": 1.115
    }
    """

    hydro_min = df["Hydrophobic"].min()
    hydro_max = df["Hydrophobic"].max()

    hbond_min = df["Hydrogen_Bond"].min()
    hbond_max = df["Hydrogen_Bond"].max()

    thresholds = {

        "hydrophobic_min": hydro_min,
        "hydrophobic_max": hydro_max,
        "hydrophobic": (hydro_min + hydro_max) / 2,
        
        
        "hbond_min": hbond_min,
        "hbond_max": hbond_max,
        "hydrogen_bond": (hbond_min + hbond_max) / 2
    }

    return thresholds


# ------------------------------------------------------------
# Encode a Single Interaction Site
# ------------------------------------------------------------

def first_encode_site(hydrophobic: float,hydrogen_bond: float,thresholds: dict) -> tuple[int, int]:
    """
    Perform the first encoding for a single interaction site.

    Parameters
    ----------
    hydrophobic : float
    hydrogen_bond : float
    thresholds : dict

    Returns
    -------
    tuple[int, int]

    Example

    (2.69,0.31)

    →

    (1,0)
    """

    hydro_bit = int(
        hydrophobic >= thresholds["hydrophobic"]
    )

    hbond_bit = int(
        hydrogen_bond >= thresholds["hydrogen_bond"]
    )

    return hydro_bit, hbond_bit

# ------------------------------------------------------------
# Encode Entire Dataset
# ------------------------------------------------------------

def encode_dataset(df,thresholds):
    """
    First encode the entire dataset.

    Returns
    -------
    pd.DataFrame
    """

    encoded = df.copy()

    encoded["Encoded"] = encoded.apply(
        lambda row:first_encode_site(row["Hydrophobic"],row["Hydrogen_Bond"],thresholds),axis=1
    )

    return encoded