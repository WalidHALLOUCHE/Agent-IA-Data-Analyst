"""Agent responsable du scoring et de l'explication de la qualité des données."""

from __future__ import annotations

import pandas as pd


class DataQualityAgent:
    name = "DataQualityAgent"
    role = "Audite la qualité des données après nettoyage."

    def run(
        self,
        raw_df: pd.DataFrame,
        cleaned_df: pd.DataFrame,
        cleaning_stats: dict[str, int],
    ) -> dict[str, object]:
        raw_rows = int(len(raw_df))
        cleaned_rows = int(len(cleaned_df))
        duplicate_rows = int(cleaned_df.duplicated().sum())
        missing_values = {column: int(value) for column, value in cleaned_df.isna().sum().items()}
        missing_cells = int(sum(missing_values.values()))
        total_cells = int(cleaned_df.shape[0] * cleaned_df.shape[1])

        empty_ratio = _ratio(cleaning_stats.get("empty_rows_removed", 0), raw_rows)
        header_ratio = _ratio(cleaning_stats.get("repeated_headers_removed", 0), raw_rows)
        invalid_ratio = _ratio(cleaning_stats.get("invalid_rows_removed", 0), raw_rows)
        duplicate_ratio = _ratio(duplicate_rows, cleaned_rows)
        missing_ratio = _ratio(missing_cells, total_cells)

        penalty = (
            min(20.0, empty_ratio * 60)
            + min(20.0, header_ratio * 80)
            + min(30.0, invalid_ratio * 100)
            + min(20.0, duplicate_ratio * 80)
            + min(20.0, missing_ratio * 100)
        )
        quality_score = round(max(0.0, 100.0 - penalty), 2)

        issues = []
        if cleaning_stats.get("empty_rows_removed", 0):
            issues.append(f"{cleaning_stats['empty_rows_removed']} lignes complètement vides ont été supprimées.")
        if cleaning_stats.get("repeated_headers_removed", 0):
            issues.append(f"{cleaning_stats['repeated_headers_removed']} lignes d'en-têtes répétés ont été supprimées.")
        if cleaning_stats.get("invalid_rows_removed", 0):
            issues.append(f"{cleaning_stats['invalid_rows_removed']} lignes sont devenues invalides après conversion des types.")
        if duplicate_rows:
            issues.append(f"{duplicate_rows} lignes doublons sont présentes après nettoyage.")
        if missing_cells:
            issues.append(f"{missing_cells} cellules manquantes restent après nettoyage.")
        if not issues:
            issues.append("Aucun problème majeur de qualité n'a été détecté après nettoyage.")

        return {
            "raw_rows": raw_rows,
            "cleaned_rows": cleaned_rows,
            "empty_rows_removed": cleaning_stats.get("empty_rows_removed", 0),
            "repeated_headers_removed": cleaning_stats.get("repeated_headers_removed", 0),
            "invalid_rows_removed": cleaning_stats.get("invalid_rows_removed", 0),
            "duplicate_rows": duplicate_rows,
            "missing_values": missing_values,
            "quality_score": quality_score,
            "issues": issues,
        }


def _ratio(value: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return value / denominator
