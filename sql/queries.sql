-- ==============================================================================
-- Automated Post-Hospital Patient Monitoring System
-- Script   : queries.sql
-- Purpose  : 10 simple analytical queries for initial exploration of the
--            [dbo].[patient_vitals] table.
-- Author   : Graduation Project Team
-- Date     : 2026-07-10
-- ==============================================================================


-- ------------------------------------------------------------------------------
-- Query 1: Count All Records
-- Returns the total number of telemetry records loaded into the table.
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_records
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 2: Average Heart Rate
-- Returns the mean heart rate across all patient readings.
-- ------------------------------------------------------------------------------
SELECT
    ROUND(AVG(CAST(heart_rate AS FLOAT)), 2) AS avg_heart_rate_bpm
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 3: Average Body Temperature
-- Returns the mean body temperature across all patient readings.
-- ------------------------------------------------------------------------------
SELECT
    ROUND(AVG(CAST(body_temperature AS FLOAT)), 2) AS avg_body_temperature_celsius
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 4: High Risk vs Low Risk Patient Count
-- Returns the number of records in each risk classification category.
-- ------------------------------------------------------------------------------
SELECT
    risk_category,
    COUNT(*) AS record_count
FROM dbo.patient_vitals
GROUP BY risk_category
ORDER BY record_count DESC;
GO


-- ------------------------------------------------------------------------------
-- Query 5: Average Oxygen Saturation
-- Returns the mean oxygen saturation level across all patient readings.
-- ------------------------------------------------------------------------------
SELECT
    ROUND(AVG(CAST(oxygen_saturation AS FLOAT)), 2) AS avg_oxygen_saturation_pct
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 6: Count of Records by Gender
-- Returns the total number of records grouped by patient gender.
-- ------------------------------------------------------------------------------
SELECT
    gender,
    COUNT(*) AS record_count
FROM dbo.patient_vitals
GROUP BY gender
ORDER BY record_count DESC;
GO


-- ------------------------------------------------------------------------------
-- Query 7: Highest Recorded Heart Rate
-- Returns the single highest heart rate value recorded across all patients.
-- ------------------------------------------------------------------------------
SELECT
    MAX(heart_rate) AS highest_heart_rate_bpm
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 8: Lowest Recorded Oxygen Saturation
-- Returns the single lowest oxygen saturation value recorded across all patients.
-- ------------------------------------------------------------------------------
SELECT
    MIN(oxygen_saturation) AS lowest_oxygen_saturation_pct
FROM dbo.patient_vitals;
GO


-- ------------------------------------------------------------------------------
-- Query 9: Records for Patients Older Than 60
-- Returns the count of telemetry records belonging to patients aged over 60.
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS records_age_over_60
FROM dbo.patient_vitals
WHERE age > 60;
GO


-- ------------------------------------------------------------------------------
-- Query 10: Latest 10 Recorded Measurements
-- Returns the 10 most recently recorded telemetry entries ordered by timestamp.
-- ------------------------------------------------------------------------------
SELECT TOP 10
    record_id,
    patient_id,
    measured_at,
    heart_rate,
    oxygen_saturation,
    risk_category
FROM dbo.patient_vitals
ORDER BY measured_at DESC;
GO
