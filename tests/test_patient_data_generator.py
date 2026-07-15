import csv

from src.simulator.patient_data_generator import LIVE_COLUMNS, PatientDataGenerator, append_record, run_simulator


def test_generated_record_matches_live_schema():
    record = PatientDataGenerator(seed=7).generate_record()
    assert list(record) == LIVE_COLUMNS
    assert 60 <= record["heart_rate"] <= 99
    assert record["risk_category"] in {"High Risk", "Low Risk"}


def test_append_record_preserves_prior_records(tmp_path):
    output = tmp_path / "live" / "readings.csv"
    generator = PatientDataGenerator(seed=1)
    append_record(output, generator.generate_record())
    append_record(output, generator.generate_record())
    with output.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))
    assert len(rows) == 2
    assert list(rows[0]) == LIVE_COLUMNS


def test_finite_run_writes_requested_number_of_records(tmp_path):
    output = tmp_path / "readings.csv"
    assert run_simulator(output, interval_seconds=0, count=2) == 2
    with output.open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == 2
