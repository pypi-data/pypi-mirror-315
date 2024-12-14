"""Handle the KeyBank data"""

import importlib.resources as pkg_resources
from typing import Mapping, Optional, Tuple, cast

import pandas as pd
from jiwer import (  # type: ignore
    Compose,
    RemoveMultipleSpaces,
    RemoveSpecificWords,
    Strip,
    SubstituteWords,
)
from pandas import DataFrame, Series

from .clean import _get_abbreviation_map, _load_stop_words, get_abbreviations_csv
from .types import Case

SEPERATOR = ","
CODE_COLUMN = "ICD10"
SYSTEM_COLUMN = "System"
CASE_COLUMNS = ["Case", CODE_COLUMN, SYSTEM_COLUMN]


def get_keybank_csv() -> DataFrame:
    """Get the KeyBank from the csv file"""

    resources = "audio_case_grade.resources"
    keybank_file = "keybank.csv"

    with pkg_resources.open_text(resources, keybank_file) as csv_file:
        return pd.read_csv(
            csv_file,
            na_filter=False,
        )


def check_for_dupes(
    keybank: DataFrame, ignore_error: Optional[bool] = False
) -> DataFrame:
    """Find all rows with duplicates"""

    def has_duplicates(row):
        seen = set()
        dupes = set()
        for col in keybank.columns:
            if col not in CASE_COLUMNS and isinstance(row[col], list):
                for item in row[col]:
                    if item in seen:
                        dupes.add(item)
                    else:
                        seen.add(item)
        has_dupes = len(dupes) > 0
        if has_dupes and not ignore_error:
            raise ValueError(
                f"Keybank case found with duplicate keywords: {row[CODE_COLUMN]} {dupes}"
            )
        return has_dupes

    return keybank[keybank.apply(has_duplicates, axis=1)]


def _clean_keybank(keybank: DataFrame, abbrev_map: Mapping[str, str]) -> DataFrame:
    stop = _load_stop_words()
    text_normalization = Compose(
        [
            RemoveSpecificWords(stop),
            SubstituteWords(abbrev_map),
            Strip(),
            RemoveMultipleSpaces(),
        ]
    )

    def clean_cell(cell):
        if pd.isna(cell):
            return []
        if isinstance(cell, str):
            cleaned = text_normalization(cell)
            return list(
                {item.strip() for item in cleaned.split(SEPERATOR) if item != ""}
            )
        return []

    cleaned_keybank = keybank.copy()

    for column in cleaned_keybank.columns:
        if column not in CASE_COLUMNS:
            cleaned_keybank[column] = cleaned_keybank[column].apply(clean_cell)

    check_for_dupes(cleaned_keybank)

    return cleaned_keybank


def _get_rows_by_code(keybank: DataFrame, case: Case) -> DataFrame:
    """Get the rows that match the case"""

    return keybank[keybank[CODE_COLUMN] == case.code]


def _get_rows_by_system(keybank: DataFrame, case: Case) -> DataFrame:
    """Get the rows that match the system but not case"""

    return keybank[keybank[SYSTEM_COLUMN] == case.system]


def _combine_rows(rows: DataFrame) -> Series:
    """Combine rows into a single row"""

    single_row_df = rows.apply(
        lambda col: list(
            {item.strip() for row in col for item in row if isinstance(row, list)}
        )
    )

    # Single row is already a series but has wrong type
    series = cast(Series, single_row_df)
    series.name = "Keywords"

    return series


def _subtract_series(s1: Series, s2: Series) -> Series:
    """Subtract the string arrays in df2 from df1."""

    return s1.combine(s2, lambda cell1, cell2: list(set(cell1) - set(cell2)))


def get_keybank(
    case: Case,
    keybank_override: Optional[DataFrame] = None,
    abbreviations_override: Optional[DataFrame] = None,
) -> Tuple[Series, Series]:
    """Get the KeyBank"""

    keybank = get_keybank_csv() if keybank_override is None else keybank_override
    abbrev = (
        get_abbreviations_csv()
        if abbreviations_override is None
        else abbreviations_override
    )
    abbrev_map = _get_abbreviation_map(abbrev)

    cleaned_keybank = _clean_keybank(keybank, abbrev_map)

    correct_rows = _get_rows_by_code(cleaned_keybank, case).drop(CASE_COLUMNS, axis=1)
    correct_row = _combine_rows(correct_rows)

    wrong_rows = _get_rows_by_system(cleaned_keybank, case).drop(CASE_COLUMNS, axis=1)
    wrong_row = _combine_rows(wrong_rows)
    wrong_row_without_correct = _subtract_series(wrong_row, correct_row)

    return correct_row, wrong_row_without_correct
