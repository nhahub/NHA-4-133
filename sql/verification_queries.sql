-- ==============================================================================
-- Automated Post-Hospital Patient Monitoring System
-- Script   : verification_queries.sql
-- Purpose  : Post-load verification queries to confirm that [dbo].[patient_vitals]
--            was populated correctly after running load_to_sql.py.
--            Run these queries in Azure Portal Query Editor, SSMS, or
--            Azure Data Studio after the data load completes.
-- Author   : Graduation Project Team
-- Date     : 2026-07-10
-- ==============================================================================


-- ------------------------------------------------------------------------------
-- Query 1: Total Row Count
-- Expected result: 200020
-- Confirms that all records from the cleaned CSV were inserted successfully.
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_rows
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 2: Top 10 Rows
-- Returns the first 10 records ordered by the surrogate primary key.
-- Use this to visually inspect column values and confirm data loaded correctly.
-- ------------------------------------------------------------------------------
SELECT TOP 10
    record_id,
    patient_id,
    measured_at,
    heart_rate,
    respiratory_rate,
    body_temperature,
    oxygen_saturation,
    systolic_bp,
    diastolic_bp,
    age,
    gender,
    weight_kg,
    height_m,
    hrv,
    risk_category,
    ingested_at
FROM dbo.patient_vitals
ORDER BY record_id ASC;
GO


-- ------------------------------------------------------------------------------
-- Query 3: Count High Risk Records
-- Expected result: approximately 105,115 (based on profiling of the source dataset).
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS high_risk_count
FROM dbo.patient_vitals
WHERE risk_category = 'High Risk';
GO


-- ------------------------------------------------------------------------------
-- Query 4: Count Low Risk Records
-- Expected result: approximately 94,905 (remaining records after High Risk).
-- Together with Query 3, both counts must sum to 200,020.
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS low_risk_count
FROM dbo.patient_vitals
WHERE risk_category = 'Low Risk';
GO


-- ------------------------------------------------------------------------------
-- Query 5: Min and Max Timestamps
-- Confirms the full date range of the telemetry data was loaded correctly.
-- Both values should reflect the actual timestamps from the cleaned CSV.
-- ------------------------------------------------------------------------------
SELECT
    MIN(measured_at) AS earliest_measurement,
    MAX(measured_at) AS latest_measurement
FROM dbo.patient_vitals;
GO
