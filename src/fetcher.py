import serpapi
import os
from datetime import datetime
import argparse
from dotenv import load_dotenv
from storage import save_raw_data

load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")
client = serpapi.Client(api_key=API_KEY)


def date_validation(date_entered):
        try:
                datetime.strptime(date_entered, "%Y-%m-%d")
                return date_entered
        except ValueError:
                raise ValueError("Enter a valid date in YYYY-MM-DD format.")
        

def get_arguments():
        parser = argparse.ArgumentParser(
                description="Fetch flight search results."
        )

        parser.add_argument(
                "--origin",
                type=str.upper,
                required=True,
                help="Origin airport code eg LOS"
        )

        parser.add_argument(
                "--destination",
                type=str.upper,
                required=True,
                help="Destination airport code eg LHS"
        )

        parser.add_argument(
        "--date",
        type=date_validation,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Outbound date: YYYY-MM-DD"
        )

        parser.add_argument(
                "--currency",
                type=str.upper,
                default="USD",
                help="Price currency"
        )

        return parser.parse_args()


def fetch_flights(origin, destination, outbound_date, currency):
        
        results = client.search({
                "engine": "google_flights",
                "departure_id": origin,
                "arrival_id": destination,
                "currency": currency,
                "type": "2",
                "outbound_date": outbound_date
        })

        return results


        

if __name__ == "__main__":
        args = get_arguments()

        results = fetch_flights(
                args.origin,
                args.destination,
                args.date,
                args.currency
        )

        save_raw_data(results)

        print("flight data saved successfully")

        print(results)