import json
import hashlib
from pathlib import Path
from datetime import datetime

RAW_DATA_PATH = Path("data/raw/flights.json")

def load_raw_data() -> list[dict]:
        """Load all previously saved flight search runs from the JSON file.

        Returns an empty list if the file doesn't exist yet.
        """
        
        if RAW_DATA_PATH.exists():
                with open(RAW_DATA_PATH, "r") as file:
                        return json.load(file)

        return []


def generate_fingerprints(results: dict) -> str:
        """Generate a SHA-256 fingerprint of the selected flight search data.

        Used to identify previously collected flight data and prevent
        duplicate collection runs from being saved.
        """

        flight_data = {
                "best_flights": results.get("best_flights", []),
                "other_flights": results.get("other_flights", []),
                "price_insights": results.get("price_insights", [])
        }

        serialized_data = json.dumps(
                flight_data,
                sort_keys=True,
                separators=(",", ":"),
                default=str
        )

        return hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()


def save_raw_data(results: dict) -> bool:
        """Save a new flight search run to the JSON file.

        Checks existing runs for duplicates using the data fingerprint.
        If a duplicate is found, skips saving. Otherwise, appends the
        new run to the existing collection history.
        """

        try:
                runs = load_raw_data()

                fingerprint = generate_fingerprints(results)

                for run in runs:
                        if run.get("fingerprint") == fingerprint:
                                print("Duplicate flight data detected. Skipping save.")
                                return False

                run = {
                        "fetched_at": datetime.now().isoformat(),
                        "fingerprint": fingerprint,
                        "results": results
                }

                runs.append(run)

                RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

                with open(RAW_DATA_PATH, "w") as file:
                        json.dump(runs, file, indent=4, default=dict)

                return True
        
        except Exception:
                raise 
