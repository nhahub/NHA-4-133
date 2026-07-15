# Dynamic Data Generation

## Purpose

The project retains its historical CSV batch-processing workflow and adds an independent live-data simulator. The simulator represents post-hospital monitoring devices by creating realistic patient vital-sign readings at a regular interval. It does not change or replace the historical dataset, Azure Data Factory, Azure Blob Storage, Azure SQL Database, SQL scripts, or the existing cleaning pipeline.

## How It Works

`src/simulator/patient_data_generator.py` keeps a pool of simulated patients with stable demographic details. Every five seconds it selects a patient, generates a new vital-sign reading, assigns a risk category, and appends the record to `data/live/live_patient_data.csv`.

The output uses the existing cleaned-data schema: `patient_id`, `heart_rate`, `respiratory_rate`, `timestamp`, `body_temperature`, `oxygen_saturation`, `systolic_blood_pressure`, `diastolic_blood_pressure`, `age`, `gender`, `weight_kg`, `height_m`, `hrv`, `risk_category`.

Generated values stay within the ranges used by the historical dataset. High-risk readings use elevated but schema-compatible heart rate, respiratory rate, and blood-pressure values.

## Run It

```powershell
python src/simulator/patient_data_generator.py
```

This runs continuously and appends one record every five seconds. Stop it with `Ctrl+C`.

For a short local demonstration:

```powershell
python src/simulator/patient_data_generator.py --count 3 --interval 0
```

The simulator creates `data/live/` and the CSV header automatically. It always appends records; it never rewrites prior readings.

## Relationship to the Existing Pipeline

The simulator is intentionally a local, standalone enhancement. The historical CSV remains the source for the current batch ETL workflow. The generated live CSV can be reviewed locally or used later as input to a separate live-ingestion path after explicit Azure design and approval. No Azure resources are deployed or changed by this module.
