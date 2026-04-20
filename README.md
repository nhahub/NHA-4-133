Automated Post-Hospital Incident Follow-up System
DEPI · ML & Data Engineering Track
==================================================

OVERVIEW
--------
Backend data pipeline for post-discharge patient monitoring.
A Python wristband simulator streams vital signs into Azure Fabric,
where ML anomaly detection, a RAG medical assistant, and a Slack
alert engine operate end-to-end — no physical hardware, no frontend.

SYSTEM STAGES
-------------
1. Simulate  — Python script publishes HR, SpO2, temp, movement,
               skin conductance via MQTT (>= 1 Hz per patient)
2. Ingest    — Azure Fabric Eventstream writes to raw_vitals Delta table
3. Curate    — Fabric Data Pipeline runs every 5 min; validates and
               partitions data into curated_vitals
4. Detect    — Fabric Spark Notebook runs MiniROCKET anomaly scoring;
               writes confirmed events to anomaly_events table
5. Answer    — FastAPI + Claude Sonnet RAG service answers patient
               queries from pgvector discharge notes
6. Alert     — Alert engine polls anomaly_events; fires Slack webhook
               for anomalies and missed-dose reminders

PREREQUISITES
-------------
- Python 3.11+
- Azure Fabric workspace (Lakehouse, Eventstream, Data Pipeline, Notebooks)
- HiveMQ Cloud account (free tier, TLS enabled)
- PostgreSQL with pgvector extension
- Slack incoming webhook URL
- Anthropic API key (Claude Sonnet)
- MIMIC-IV access via PhysioNet (CITI training required)

ENVIRONMENT VARIABLES
---------------------
Copy .env.example to .env and fill in:

  MQTT_BROKER_URL            HiveMQ Cloud broker hostname
  MQTT_PORT                  8883 (TLS)
  MQTT_USERNAME
  MQTT_PASSWORD
  FABRIC_LAKEHOUSE_URL       Fabric SQL endpoint URL
  FABRIC_TENANT_ID
  FABRIC_CLIENT_ID
  FABRIC_CLIENT_SECRET
  PGVECTOR_URL               PostgreSQL connection string
  ANTHROPIC_API_KEY
  SLACK_WEBHOOK_URL
  RAG_CONFIDENCE_THRESHOLD   0.6 (default)

INSTALLATION
------------
  pip install -r requirements.txt

RUNNING THE SIMULATOR
---------------------
  python simulator/run.py --profiles config/patients.json
  python simulator/run.py --profiles config/patients.json --inject-anomaly
  python simulator/run.py --profiles config/patients.json --dropout 30

AZURE FABRIC SETUP
------------------
1. Create a Fabric Lakehouse and note the SQL endpoint URL.
2. Configure an Eventstream with HiveMQ as the MQTT source and
   raw_vitals Delta table as the destination.
3. Import pipelines/raw_to_curated.json and set a 5-minute trigger.
4. Upload and run notebooks/anomaly_detection.ipynb.
   First run trains MiniROCKET on MIMIC-IV (~8 min).
   Subsequent runs score new curated_vitals windows.

RAG SERVICE
-----------
  python rag/load_notes.py --synthea-dir data/synthea/
  uvicorn rag.main:app --host 0.0.0.0 --port 8000

  POST /query
  Body: { "patient_id": "<uuid>", "query": "What are my discharge medications?" }

ALERT ENGINE
------------
  python alerts/engine.py

Polls anomaly_events every 30 s. Fires Slack alerts for anomalies
and missed-dose notifications after 3 consecutive unconfirmed doses.

END-TO-END INTEGRATION TEST
----------------------------
  python tests/test_e2e.py

Injects a known anomaly and asserts all KPIs across every stage.
Full pipeline target: simulator -> Slack alert < 3 min.

DELTA TABLE SCHEMA
------------------
  raw_vitals           patient_id, parameter, value, ts
  curated_vitals       same + motion_artefact_flag (bool)
  anomaly_events       patient_id, parameter, anomaly_score, threshold, window_start
  medication_schedule  patient_id, medication, dose_time, supply_count
  alert_log            alert_type, ts, delivered (bool), message_payload
  discharge_notes      pgvector — patient_id, chunk_text, embedding, source_section

DATASETS
--------
  MIMIC-IV Vitals    PhysioNet — model training/evaluation (CITI access required)
  NHANES 2017-2020   CDC/NIH — baseline distributions for simulator profiles (public)
  Synthea patients   MITRE — synthetic discharge notes and schedules (open-source)

No real patient data is used at any stage.

KEY PERFORMANCE TARGETS
-----------------------
  Ingest latency        < 500 ms (p95)
  ETL pipeline run      < 2 min for 100k rows
  Anomaly detection F1  >= 0.85 on MIMIC-IV held-out set
  Anomaly scoring       < 200 ms per 60-second window
  RAG response          < 10 s (p95)
  Alert delivery        < 60 s from anomaly_event write
  End-to-end pipeline   < 3 min (anomaly inject -> Slack alert)

SECURITY NOTES
--------------
- MQTT traffic uses TLS 1.3 (enforced by HiveMQ Cloud).
- Fabric workspace access restricted via Azure AD RBAC.
- Patient IDs are UUIDs with no link to real identity.
- pgvector store accessible only by the FastAPI service account.
- alert_log records retained in full through M5.

TEAM ROLES
----------
  Simulator Engineer   Python simulator, MQTT publisher, anomaly injection
  ML Engineer          MiniROCKET notebook, MIMIC-IV preprocessing, baselines
  AI/Backend Engineer  RAG pipeline, Claude Sonnet integration, FastAPI service
  Data Engineer        Lakehouse schema, Eventstream config, ETL pipeline
  DevOps/Integration   MQTT broker, Fabric config, CI script, e2e test
  Project Lead/QA      Architecture, cross-component review, docs, demo
