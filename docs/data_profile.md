# Data Profiling Report: Human Vital Signs Dataset 2024

This profiling report summarizes the raw dataset: `human_vital_signs_dataset_2024.csv` to guide design decisions for cleaning, transforming, and database ingestion.

## 1. Dataset Overview

- **File Path**: `data/raw/human_vital_signs_dataset_2024.csv`
- **Total Records (Rows)**: 200,020
- **Total Columns**: 17
- **Duplicate Rows**: 0 (0.00%)

---

## 2. Schema and Completeness

Below is the list of columns, their data types, null counts, and unique value counts:

| Column Name              | Data Type   |   Missing Values | Missing %   |   Unique Values |
|:-------------------------|:------------|-----------------:|:------------|----------------:|
| Patient ID               | int64       |                0 | 0.00%       |          200020 |
| Heart Rate               | int64       |                0 | 0.00%       |              40 |
| Respiratory Rate         | int64       |                0 | 0.00%       |               8 |
| Timestamp                | str         |                0 | 0.00%       |          200020 |
| Body Temperature         | float64     |                0 | 0.00%       |          200020 |
| Oxygen Saturation        | float64     |                0 | 0.00%       |          200020 |
| Systolic Blood Pressure  | int64       |                0 | 0.00%       |              30 |
| Diastolic Blood Pressure | int64       |                0 | 0.00%       |              20 |
| Age                      | int64       |                0 | 0.00%       |              72 |
| Gender                   | str         |                0 | 0.00%       |               2 |
| Weight (kg)              | float64     |                0 | 0.00%       |          200020 |
| Height (m)               | float64     |                0 | 0.00%       |          200020 |
| Derived_HRV              | float64     |                0 | 0.00%       |          200020 |
| Derived_Pulse_Pressure   | int64       |                0 | 0.00%       |              49 |
| Derived_BMI              | float64     |                0 | 0.00%       |          200020 |
| Derived_MAP              | float64     |                0 | 0.00%       |              87 |
| Risk Category            | str         |                0 | 0.00%       |               2 |

---

## 3. Statistical Summaries

### Numeric Columns Summary

| Column Name              |   count |           mean |           std |         min |           25% |            50% |           75% |           max |
|:-------------------------|--------:|---------------:|--------------:|------------:|--------------:|---------------:|--------------:|--------------:|
| Patient ID               |  200020 | 100010         | 57740.9       |   1         | 50005.8       | 100010         | 150015        | 200020        |
| Heart Rate               |  200020 |     79.5337    |    11.5529    |  60         |    70         |     80         |     90        |     99        |
| Respiratory Rate         |  200020 |     15.4895    |     2.29447   |  12         |    13         |     15         |     17        |     19        |
| Body Temperature         |  200020 |     36.7484    |     0.43329   |  36         |    36.3726    |     36.7477    |     37.123    |     37.5      |
| Oxygen Saturation        |  200020 |     97.5044    |     1.4426    |  95         |    96.2569    |     97.5096    |     98.7557   |    100        |
| Systolic Blood Pressure  |  200020 |    124.438     |     8.65695   | 110         |   117         |    124         |    132        |    139        |
| Diastolic Blood Pressure |  200020 |     79.4996    |     5.75725   |  70         |    75         |     79         |     84        |     89        |
| Age                      |  200020 |     53.4463    |    20.7868    |  18         |    35         |     53         |     71        |     89        |
| Weight (kg)              |  200020 |     74.9964    |    14.4715    |  50.0002    |    62.4236    |     74.9772    |     87.5395   |     99.9998   |
| Height (m)               |  200020 |      1.75003   |     0.144554  |   1.5       |     1.62478   |      1.75048   |      1.87531  |      2        |
| Derived_HRV              |  200020 |      0.0999703 |     0.0288606 |   0.0500003 |     0.0749547 |      0.0999877 |      0.124917 |      0.149999 |
| Derived_Pulse_Pressure   |  200020 |     44.9383    |    10.4049    |  21         |    37         |     45         |     53        |     69        |
| Derived_BMI              |  200020 |     25.0036    |     6.44714   |  12.506     |    20.1344    |     24.3208    |     29.1872   |     44.3765   |
| Derived_MAP              |  200020 |     94.4791    |     4.79789   |  83.3333    |    91         |     94.3333    |     98        |    105.667    |

### Non-Numeric Columns Summary

| Column Name   |   count |   unique | top                        |   freq |
|:--------------|--------:|---------:|:---------------------------|-------:|
| Timestamp     |  200020 |   200020 | 2024-07-19 21:53:45.729841 |      1 |
| Gender        |  200020 |        2 | Female                     | 100117 |
| Risk Category |  200020 |        2 | High Risk                  | 105115 |

---

## 4. Sample Records (First 5 Rows)

|   Patient ID |   Heart Rate |   Respiratory Rate | Timestamp                  |   Body Temperature |   Oxygen Saturation |   Systolic Blood Pressure |   Diastolic Blood Pressure |   Age | Gender   |   Weight (kg) |   Height (m) |   Derived_HRV |   Derived_Pulse_Pressure |   Derived_BMI |   Derived_MAP | Risk Category   |
|-------------:|-------------:|-------------------:|:---------------------------|-------------------:|--------------------:|--------------------------:|---------------------------:|------:|:---------|--------------:|-------------:|--------------:|-------------------------:|--------------:|--------------:|:----------------|
|            1 |           60 |                 12 | 2024-07-19 21:53:45.729841 |            36.8617 |             95.702  |                       124 |                         86 |    37 | Female   |       91.5416 |      1.67935 |     0.121033  |                       38 |       32.459  |       98.6667 | High Risk       |
|            2 |           63 |                 18 | 2024-07-19 21:52:45.729841 |            36.5116 |             96.6894 |                       126 |                         84 |    77 | Male     |       50.7049 |      1.99255 |     0.117062  |                       42 |       12.7712 |       98      | High Risk       |
|            3 |           63 |                 15 | 2024-07-19 21:51:45.729841 |            37.052  |             98.5083 |                       131 |                         78 |    68 | Female   |       90.3168 |      1.77023 |     0.0532    |                       53 |       28.8211 |       95.6667 | Low Risk        |
|            4 |           99 |                 16 | 2024-07-19 21:50:45.729841 |            36.6547 |             95.0118 |                       118 |                         72 |    41 | Female   |       96.0062 |      1.83363 |     0.0644747 |                       46 |       28.5546 |       87.3333 | High Risk       |
|            5 |           69 |                 16 | 2024-07-19 21:49:45.729841 |            36.9751 |             98.6238 |                       138 |                         76 |    25 | Female   |       56.02   |      1.86642 |     0.118484  |                       62 |       16.0814 |       96.6667 | High Risk       |
