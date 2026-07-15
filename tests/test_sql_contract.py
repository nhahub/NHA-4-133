from pathlib import Path


def test_schema_has_duplicate_and_domain_protection():
    ddl = (Path("sql") / "create_patient_vitals.sql").read_text(encoding="utf-8")
    assert "UQ_patient_vitals_patient_measurement" in ddl
    assert "CK_patient_vitals_risk_category" in ddl
