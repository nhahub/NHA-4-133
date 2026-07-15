"""Append simulated live patient vital-sign readings to a local CSV file."""

from __future__ import annotations

import argparse
import csv
import logging
import random
import time
from datetime import datetime
from pathlib import Path


LOGGER = logging.getLogger(__name__)
LIVE_COLUMNS = [
    "patient_id", "heart_rate", "respiratory_rate", "timestamp",
    "body_temperature", "oxygen_saturation", "systolic_blood_pressure",
    "diastolic_blood_pressure", "age", "gender", "weight_kg", "height_m",
    "hrv", "risk_category",
]


class PatientDataGenerator:
    """Generate clinically plausible readings for a fixed pool of simulated patients."""

    def __init__(self, patient_count: int = 100, seed: int | None = None) -> None:
        if patient_count < 1:
            raise ValueError("patient_count must be at least 1.")
        self.random = random.Random(seed)
        self.patients = {
            patient_id: self._create_patient_profile(patient_id)
            for patient_id in range(300_001, 300_001 + patient_count)
        }

    def _create_patient_profile(self, patient_id: int) -> dict[str, int | float | str]:
        return {
            "patient_id": patient_id,
            "age": self.random.randint(18, 89),
            "gender": self.random.choice(["Female", "Male"]),
            "weight_kg": round(self.random.uniform(50.0, 100.0), 2),
            "height_m": round(self.random.uniform(1.50, 2.00), 2),
        }

    def generate_record(self) -> dict[str, int | float | str]:
        """Create one reading using the same value ranges as the historical dataset."""
        profile = self.patients[self.random.choice(list(self.patients))]
        elevated = self.random.random() < 0.30
        if elevated:
            heart_rate, respiratory_rate = self.random.randint(90, 99), self.random.randint(16, 19)
            oxygen_saturation = round(self.random.uniform(95.0, 97.0), 2)
            systolic_bp, diastolic_bp, risk_category = self.random.randint(130, 139), self.random.randint(82, 89), "High Risk"
        else:
            heart_rate, respiratory_rate = self.random.randint(60, 89), self.random.randint(12, 16)
            oxygen_saturation = round(self.random.uniform(97.0, 100.0), 2)
            systolic_bp, diastolic_bp, risk_category = self.random.randint(110, 129), self.random.randint(70, 81), "Low Risk"

        return {
            "patient_id": profile["patient_id"], "heart_rate": heart_rate,
            "respiratory_rate": respiratory_rate,
            "timestamp": datetime.now().isoformat(sep=" ", timespec="microseconds"),
            "body_temperature": round(self.random.uniform(36.0, 37.5), 2),
            "oxygen_saturation": oxygen_saturation, "systolic_blood_pressure": systolic_bp,
            "diastolic_blood_pressure": diastolic_bp, "age": profile["age"],
            "gender": profile["gender"], "weight_kg": profile["weight_kg"],
            "height_m": profile["height_m"], "hrv": round(self.random.uniform(0.05, 0.15), 4),
            "risk_category": risk_category,
        }


def append_record(output_path: Path, record: dict[str, int | float | str]) -> None:
    """Append one record and create the destination with a header when needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not output_path.exists() or output_path.stat().st_size == 0
    with output_path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=LIVE_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(record)


def run_simulator(output_path: Path, interval_seconds: float = 5.0, count: int | None = None) -> int:
    """Generate records until interrupted, or until ``count`` records are written."""
    if interval_seconds < 0:
        raise ValueError("interval_seconds cannot be negative.")
    if count is not None and count < 1:
        raise ValueError("count must be at least 1 when provided.")
    generator, written = PatientDataGenerator(), 0
    LOGGER.info("Writing simulated readings to %s", output_path)
    try:
        while count is None or written < count:
            append_record(output_path, generator.generate_record())
            written += 1
            LOGGER.info("Generated Record #%d", written)
            if count is None or written < count:
                time.sleep(interval_seconds)
    except KeyboardInterrupt:
        LOGGER.info("Simulator stopped after %d records.", written)
    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate append-only simulated patient vital-sign readings.")
    parser.add_argument("--output", type=Path, default=Path("data/live/live_patient_data.csv"))
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between readings (default: 5).")
    parser.add_argument("--count", type=int, help="Optional number of readings for a finite demo run.")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    args = parse_args()
    run_simulator(args.output, args.interval, args.count)
