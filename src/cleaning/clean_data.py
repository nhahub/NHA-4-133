from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

import pandas as pd

RAW_REQUIRED_COLUMNS = {
    "Patient ID", "Heart Rate", "Respiratory Rate", "Timestamp",
    "Body Temperature", "Oxygen Saturation", "Systolic Blood Pressure",
    "Diastolic Blood Pressure", "Age", "Gender", "Weight (kg)",
    "Height (m)", "Derived_HRV", "Risk Category",
}

RENAME_MAPPING = {
    'Patient ID': 'patient_id', 'Heart Rate': 'heart_rate',
    'Respiratory Rate': 'respiratory_rate', 'Timestamp': 'timestamp',
    'Body Temperature': 'body_temperature', 'Oxygen Saturation': 'oxygen_saturation',
    'Systolic Blood Pressure': 'systolic_blood_pressure',
    'Diastolic Blood Pressure': 'diastolic_blood_pressure', 'Age': 'age',
    'Gender': 'gender', 'Weight (kg)': 'weight_kg', 'Height (m)': 'height_m',
    'Derived_HRV': 'hrv', 'Risk Category': 'risk_category',
}

EXPECTED_COLUMNS = list(RENAME_MAPPING.values())
NUMERIC_RANGES = {
    "heart_rate": (20, 250), "respiratory_rate": (5, 80),
    "body_temperature": (25, 45), "oxygen_saturation": (0, 100),
    "systolic_blood_pressure": (50, 250), "diastolic_blood_pressure": (30, 180),
    "age": (0, 130), "weight_kg": (2, 500), "height_m": (0.3, 3.0),
    "hrv": (0, 10),
}


def validate_raw_dataframe(df: pd.DataFrame) -> None:
    missing = sorted(RAW_REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError(f"Raw dataset is missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Raw dataset is empty.")


def validate_clean_dataframe(df: pd.DataFrame) -> None:
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError("Cleaned schema does not match the expected 14-column schema.")
    if df.isna().any().any():
        null_columns = df.columns[df.isna().any()].tolist()
        raise ValueError(f"Cleaned dataset contains null values: {', '.join(null_columns)}")
    if df.duplicated().any():
        raise ValueError("Cleaned dataset contains duplicate records.")
    invalid_ranges = []
    for column, (minimum, maximum) in NUMERIC_RANGES.items():
        invalid = ~df[column].between(minimum, maximum)
        if invalid.any():
            invalid_ranges.append(column)
    if invalid_ranges:
        raise ValueError(f"Values outside accepted ranges: {', '.join(invalid_ranges)}")
    if not set(df["gender"].unique()).issubset({"Male", "Female"}):
        raise ValueError("gender must contain only 'Male' or 'Female'.")
    if not set(df["risk_category"].unique()).issubset({"High Risk", "Low Risk"}):
        raise ValueError("risk_category must contain only 'High Risk' or 'Low Risk'.")


def clean_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Apply the documented transformations and reject invalid input data."""
    validate_raw_dataframe(raw_df)
    df = raw_df.copy()
    df = df.drop(columns=['Derived_BMI', 'Derived_MAP', 'Derived_Pulse_Pressure'], errors='ignore')
    df = df.rename(columns=RENAME_MAPPING)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='raise')
    for column in NUMERIC_RANGES:
        df[column] = pd.to_numeric(df[column], errors='raise')
    validate_clean_dataframe(df)
    return df


def clean_dataset(raw_path: Path | None = None, output_path: Path | None = None, report_path: Path | None = None) -> pd.DataFrame:
    project_root = Path(__file__).resolve().parents[2]
    raw_path = raw_path or project_root / "data" / "raw" / "human_vital_signs_dataset_2024.csv"
    output_path = output_path or project_root / "data" / "processed" / "patient_vitals_clean.csv"
    report_path = report_path or project_root / "docs" / "data_cleaning_report.md"

    print(f"Reading raw dataset from: {raw_path}")
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")
    raw_df = pd.read_csv(raw_path)
    original_shape = raw_df.shape
    original_cols = list(raw_df.columns)
    print("Cleaning, standardizing, and validating data...")
    df = clean_dataframe(raw_df)

    # Verify datatypes after cleaning
    final_shape = df.shape
    final_cols = list(df.columns)

    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving cleaned dataset to: {output_path}")
    df.to_csv(output_path, index=False)
    print("Cleaned dataset saved successfully.")

    # Write cleaning report
    generate_cleaning_report(str(report_path), original_shape, final_shape, original_cols, final_cols, df)
    return df

def generate_cleaning_report(report_path, orig_shape, final_shape, orig_cols, final_cols, df):
    # Get column summaries
    col_info = []
    for col in df.columns:
        col_info.append({
            'Column Name': col,
            'Data Type': str(df[col].dtype),
            'Non-Null Count': df[col].count(),
            'Memory Usage (Bytes)': df[col].memory_usage(index=False, deep=True)
        })
    col_info_df = pd.DataFrame(col_info)
    col_info_md = col_info_df.to_markdown(index=False)
    
    report_content = f"""# Data Cleaning Report
**Project**: Automated Post-Hospital Patient Monitoring System  
**Pipeline Step**: Ingestion & Data Cleaning  
**Generated On**: {date.today().isoformat()}  

---

## 1. Summary of Actions & Transformations

A Python data cleaning pipeline was executed on the raw dataset. The pipeline applied the following transformations:

1. **Dropped Redundant Derived Columns**: 
   - `Derived_BMI`
   - `Derived_MAP`
   - `Derived_Pulse_Pressure`
   - *Justification*: Removed to enforce normalization, minimize database storage requirements, and eliminate write anomalies in the target table.

2. **Renamed Columns to `snake_case`**:
   - Mapped all mixed-case and bracketed columns to a consistent lowercase snake_case standard (e.g., `Patient ID` $\\rightarrow$ `patient_id`, `Weight (kg)` $\\rightarrow$ `weight_kg`).

3. **Casted Timestamp String to Datetime**:
   - Converted the `Timestamp` column into a proper Pandas `datetime64[ns]` object to support timeseries indexing and partition queries.

4. **Kept Target Columns**:
   - Retained `hrv` (renamed from `Derived_HRV`) for detailed sensor analysis.
   - Retained `risk_category` for ground-truth comparison and evaluation.

---

## 2. Dataset Shape Changes

- **Original Dimensions**: {orig_shape[0]:,} rows, {orig_shape[1]} columns
- **Cleaned Dimensions**: {final_shape[0]:,} rows, {final_shape[1]} columns
- **Removed Columns**: {orig_shape[1] - final_shape[1]} columns (`Derived_BMI`, `Derived_MAP`, `Derived_Pulse_Pressure`)

---

## 3. Cleaned Dataset Schema

Below is the verified schema and description of the processed data:

{col_info_md}

---

## 4. Sample Cleaned Data (First 5 Rows)

{df.head(5).to_markdown(index=False)}
"""
    print(f"Writing data cleaning report to: {report_path}")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Report written successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and validate patient vital-signs data.")
    parser.add_argument("--input", type=Path, help="Raw CSV path")
    parser.add_argument("--output", type=Path, help="Clean CSV path")
    args = parser.parse_args()
    clean_dataset(args.input, args.output)
