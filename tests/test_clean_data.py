from pathlib import Path

import pandas as pd
import pytest

from src.cleaning.clean_data import EXPECTED_COLUMNS, clean_dataframe


def raw_record(**overrides):
    record = {
        "Patient ID": 1, "Heart Rate": 75, "Respiratory Rate": 16,
        "Timestamp": "2024-07-19 21:53:45.729841", "Body Temperature": 36.7,
        "Oxygen Saturation": 98.0, "Systolic Blood Pressure": 120,
        "Diastolic Blood Pressure": 80, "Age": 42, "Gender": "Male",
        "Weight (kg)": 70.0, "Height (m)": 1.75, "Derived_HRV": 0.08,
        "Derived_Pulse_Pressure": 40, "Derived_BMI": 22.86, "Derived_MAP": 93.33,
        "Risk Category": "Low Risk",
    }
    record.update(overrides)
    return record


def test_clean_dataframe_transforms_expected_columns():
    result = clean_dataframe(pd.DataFrame([raw_record()]))
    assert list(result.columns) == EXPECTED_COLUMNS
    assert result.loc[0, "timestamp"] == pd.Timestamp("2024-07-19 21:53:45.729841")
    assert "Derived_BMI" not in result.columns


def test_clean_dataframe_rejects_missing_column():
    record = raw_record()
    del record["Patient ID"]
    with pytest.raises(ValueError, match="missing required columns"):
        clean_dataframe(pd.DataFrame([record]))


def test_clean_dataframe_rejects_invalid_value_range():
    with pytest.raises(ValueError, match="heart_rate"):
        clean_dataframe(pd.DataFrame([raw_record(**{"Heart Rate": 400})]))


def test_clean_dataframe_rejects_duplicate_rows():
    frame = pd.DataFrame([raw_record(), raw_record()])
    with pytest.raises(ValueError, match="duplicate"):
        clean_dataframe(frame)
