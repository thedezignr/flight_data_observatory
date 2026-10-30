import json
from pathlib import Path
from datetime import datetime

RAW_DATA_PATH = Path("data/raw/flights.json")

def load_raw_data():
        if RAW_DATA_PATH.exists():
                with open(RAW_DATA_PATH, "r") as file:
                        return json.load(file)

        return []


def save_raw_data(results):
        try:
                runs = load_raw_data()

                run = {
                        "fetched_at": datetime.now().isoformat(),
                        "results": results
                }

                runs.append(run)

                RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

                with open(RAW_DATA_PATH, "w") as file:
                        json.dump(runs, file, indent=4, default=dict)
        except Exception:
                raise 
