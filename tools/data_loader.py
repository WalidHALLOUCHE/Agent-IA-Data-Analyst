"""Helpers de chargement du dataset."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = PROJECT_ROOT / "data" / "Sales_April_2019.csv"


def load_default_sales_data(path: Path | str = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Jeu de données introuvable : {dataset_path}")
    return pd.read_csv(dataset_path)


def load_uploaded_sales_data(file: BinaryIO) -> pd.DataFrame:
    return pd.read_csv(file)
