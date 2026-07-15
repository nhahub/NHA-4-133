# Data Cleaning Report
**Project**: Automated Post-Hospital Patient Monitoring System  
**Pipeline Step**: Ingestion & Data Cleaning  
**Generated On**: 2026-07-11  

---

## 1. Summary of Actions & Transformations

A Python data cleaning pipeline was executed on the raw dataset. The pipeline applied the following transformations:

1. **Dropped Redundant Derived Columns**: 
   - `Derived_BMI`
   - `Derived_MAP`
   - `Derived_Pulse_Pressure`
   - *Justification*: Removed to enforce normalization, minimize database storage requirements, and eliminate write anomalies in the target table.

2. **Renamed Columns to `snake_case`**:
   - Mapped all mixed-case and bracketed columns to a consistent lowercase snake_case standard (e.g., `Patient ID` $\rightarrow$ `patient_id`, `Weight (kg)` $\rightarrow$ `weight_kg`).

3. **Casted Timestamp String to Datetime**:
   - Converted the `Timestamp` column into a proper Pandas `datetime64[ns]` object to support timeseries indexing and partition queries.

4. **Kept Target Columns**:
   - Retained `hrv` (renamed from `Derived_HRV`) for detailed sensor analysis.
   - Retained `risk_category` for ground-truth comparison and evaluation.

---

## 2. Dataset Shape Changes

- **Original Dimensions**: 200,020 rows, 17 columns
- **Cleaned Dimensions**: 200,020 rows, 14 columns
- **Removed Columns**: 3 columns (`Derived_BMI`, `Derived_MAP`, `Derived_Pulse_Pressure`)

---

## 3. Cleaned Dataset Schema

Below is the verified schema and description of the processed data:

| Column Name              | Data Type      |   Non-Null Count |   Memory Usage (Bytes) |
|:-------------------------|:---------------|-----------------:|-----------------------:|
| patient_id               | int64          |           200020 |                1600160 |
| heart_rate               | int64          |           200020 |                1600160 |
| respiratory_rate         | int64          |           200020 |                1600160 |
| timestamp                | datetime64[us] |           200020 |                1600160 |
| body_temperature         | float64        |           200020 |                1600160 |
| oxygen_saturation        | float64        |           200020 |                1600160 |
| systolic_blood_pressure  | int64          |           200020 |                1600160 |
| diastolic_blood_pressure | int64          |           200020 |                1600160 |
| age                      | int64          |           200020 |                1600160 |
| gender                   | str            |           200020 |               10801294 |
| weight_kg                | float64        |           200020 |                1600160 |
| height_m                 | float64        |           200020 |                1600160 |
| hrv                      | float64        |           200020 |                1600160 |
| risk_category            | str            |           200020 |               11506255 |

---

## 4. Sample Cleaned Data (First 5 Rows)

|   patient_id |   heart_rate |   respiratory_rate | timestamp                  |   body_temperature |   oxygen_saturation |   systolic_blood_pressure |   diastolic_blood_pressure |   age | gender   |   weight_kg |   height_m |       hrv | risk_category   |
|-------------:|-------------:|-------------------:|:---------------------------|-------------------:|--------------------:|--------------------------:|---------------------------:|------:|:---------|------------:|-----------:|----------:|:----------------|
|            1 |           60 |                 12 | 2024-07-19 21:53:45.729841 |            36.8617 |             95.702  |                       124 |                         86 |    37 | Female   |     91.5416 |    1.67935 | 0.121033  | High Risk       |
|            2 |           63 |                 18 | 2024-07-19 21:52:45.729841 |            36.5116 |             96.6894 |                       126 |                         84 |    77 | Male     |     50.7049 |    1.99255 | 0.117062  | High Risk       |
|            3 |           63 |                 15 | 2024-07-19 21:51:45.729841 |            37.052  |             98.5083 |                       131 |                         78 |    68 | Female   |     90.3168 |    1.77023 | 0.0532    | Low Risk        |
|            4 |           99 |                 16 | 2024-07-19 21:50:45.729841 |            36.6547 |             95.0118 |                       118 |                         72 |    41 | Female   |     96.0062 |    1.83363 | 0.0644747 | High Risk       |
|            5 |           69 |                 16 | 2024-07-19 21:49:45.729841 |            36.9751 |             98.6238 |                       138 |                         76 |    25 | Female   |     56.02   |    1.86642 | 0.118484  | High Risk       |
