-- ==============================================================================
-- Automated Post-Hospital Patient Monitoring System
-- Script   : drop_patient_vitals.sql
-- Purpose  : Safely drops the [dbo].[patient_vitals] table if it exists.
--            Run this script before re-deploying create_patient_vitals.sql
--            to reset the schema to a clean state.
-- Author   : Graduation Project Team
-- Date     : 2026-07-10
-- WARNING  : This operation is IRREVERSIBLE. All data inside the table will
--            be permanently deleted. Do NOT run against production unless
--            a verified backup has been taken.
-- ==============================================================================

IF OBJECT_ID('dbo.patient_vitals', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.patient_vitals;
    PRINT 'Table [dbo].[patient_vitals] dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table [dbo].[patient_vitals] does not exist. No action taken.';
END
GO
