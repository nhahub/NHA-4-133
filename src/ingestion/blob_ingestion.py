"""Download a CSV from Azure Blob Storage into the raw landing directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient


def download_blob(connection_string: str, container: str, blob_name: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    client = BlobServiceClient.from_connection_string(connection_string)
    with destination.open("wb") as output:
        output.write(client.get_blob_client(container=container, blob=blob_name).download_blob().readall())
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a raw vital-signs CSV from Azure Blob Storage.")
    parser.add_argument("--blob", required=True, help="Blob name, for example incoming/vitals.csv")
    parser.add_argument("--output", type=Path, default=Path("data/raw/human_vital_signs_dataset_2024.csv"))
    args = parser.parse_args()
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container = os.getenv("AZURE_STORAGE_CONTAINER_RAW")
    if not connection_string or not container:
        raise SystemExit("AZURE_STORAGE_CONNECTION_STRING and AZURE_STORAGE_CONTAINER_RAW must be configured.")
    print(download_blob(connection_string, container, args.blob, args.output))
