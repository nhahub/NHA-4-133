-- ==============================================================================
-- Automated Post-Hospital Patient Monitoring System
-- Script   : create_patient_vitals.sql
-- Purpose  : Creates the production table [dbo].[patient_vitals] in Azure SQL
--            Database. This is the single flat staging table that receives
--            cleaned telemetry records from the Python cleaning pipeline.
-- Author   : Graduation Project Team
-- Date     : 2026-07-10
-- ==============================================================================

CREATE TABLE dbo.patient_vitals (

    -- -------------------------------------------------------------------------
    -- Surrogate Primary Key
    -- -------------------------------------------------------------------------
    record_id               INT             IDENTITY(1,1)   NOT NULL,

    -- -------------------------------------------------------------------------
    -- Patient Identifier
    -- -------------------------------------------------------------------------
    patient_id              INT                             NOT NULL,

    -- -------------------------------------------------------------------------
    -- Measurement Timestamp
    -- High-precision DATETIME2(6) to preserve microsecond telemetry resolution.
    -- -------------------------------------------------------------------------
    measured_at             DATETIME2(6)                    NOT NULL,

    -- -------------------------------------------------------------------------
    -- Vital Sign Measurements
    -- SMALLINT (2 bytes) used where integer ranges allow, saving storage at
    -- scale.  DECIMAL types used for continuous readings to avoid the rounding
    -- errors introduced by binary floating-point (FLOAT) representation.
    -- -------------------------------------------------------------------------
    heart_rate              SMALLINT                        NOT NULL,   -- bpm, range 60-99
    respiratory_rate        SMALLINT                        NOT NULL,   -- breaths/min, range 12-19
    body_temperature        DECIMAL(4, 2)                   NOT NULL,   -- Celsius, range 36.00-37.50
    oxygen_saturation       DECIMAL(5, 2)                   NOT NULL,   -- %, range 95.00-100.00
    systolic_bp             SMALLINT                        NOT NULL,   -- mmHg, range 110-139
    diastolic_bp            SMALLINT                        NOT NULL,   -- mmHg, range 70-89
    hrv                     DECIMAL(5, 4)                   NOT NULL,   -- Heart Rate Variability, range 0.0500-0.1499

    -- -------------------------------------------------------------------------
    -- Patient Demographics
    -- -------------------------------------------------------------------------
    age                     SMALLINT                        NOT NULL,   -- years, range 18-89
    gender                  VARCHAR(10)                     NOT NULL,   -- 'Male' or 'Female'
    weight_kg               DECIMAL(5, 2)                   NOT NULL,   -- kg, range 50.00-99.99
    height_m                DECIMAL(3, 2)                   NOT NULL,   -- metres, range 1.50-2.00

    -- -------------------------------------------------------------------------
    -- Clinical Classification
    -- -------------------------------------------------------------------------
    risk_category           VARCHAR(20)                     NOT NULL,   -- 'High Risk' or 'Low Risk'

    -- -------------------------------------------------------------------------
    -- Audit Column
    -- Automatically records the UTC timestamp at which each row was loaded.
    -- -------------------------------------------------------------------------
    ingested_at             DATETIME2       CONSTRAINT DF_patient_vitals_ingested_at
                                            DEFAULT SYSUTCDATETIME()    NOT NULL,

    -- -------------------------------------------------------------------------
    -- Constraints
    -- -------------------------------------------------------------------------
    CONSTRAINT PK_patient_vitals PRIMARY KEY CLUSTERED (record_id),
    CONSTRAINT UQ_patient_vitals_patient_measurement UNIQUE (patient_id, measured_at),
    CONSTRAINT CK_patient_vitals_gender CHECK (gender IN ('Male', 'Female')),
    CONSTRAINT CK_patient_vitals_risk_category CHECK (risk_category IN ('High Risk', 'Low Risk')),
    CONSTRAINT CK_patient_vitals_oxygen_saturation CHECK (oxygen_saturation BETWEEN 0 AND 100)

);
GO
