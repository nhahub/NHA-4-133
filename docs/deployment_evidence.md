# Cloud Deployment Evidence

This repository contains deployable Azure SQL and Azure Data Factory artifacts. Complete this record after performing the cloud deployment; do not replace evidence with credentials or screenshots containing secrets.

| Item | Required evidence | Status |
| --- | --- | --- |
| Azure SQL schema | UTC deployment time and `INFORMATION_SCHEMA.TABLES` result | Pending |
| Data load | ADF pipeline run ID, run time, and copied-row count | Pending |
| SQL verification | Output from all queries in `sql/verification_queries.sql` | Pending |
| Event trigger | Trigger name, start time, and one successful CSV-upload run ID | Pending |
| Re-run protection | Evidence that a duplicate file does not create duplicate clinical records | Pending |

## Deployment Procedure

1. Deploy the ADF ARM templates using secure values for the Blob connection string and SQL password. Set `storageAccountResourceId` to the full Azure Storage Account resource ID.
2. Run `sql/create_patient_vitals.sql` once. The unique constraint protects the patient/timestamp business key.
3. Execute `pl_copy_raw_to_sql` manually with a single CSV and save its run ID and copied-row count above.
4. Run every query in `sql/verification_queries.sql` and attach or paste sanitized results in the submission evidence.
5. Start `trg_raw_csv_created` only after the manual run is verified. Upload a new CSV once, capture its run ID, and verify the database results.

## Important Limits

The current ADF Copy Activity performs the documented raw-to-target field mapping and excludes the three redundant source columns. The Python validation pipeline is a separate, local execution path. Do not state that ADF executes `clean_data.py` unless a supported Azure Batch, Function App, Databricks, or other compute activity has been deployed and evidenced.
