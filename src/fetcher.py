import serpapi
import os
from datetime import datetime
import argparse
from dotenv import load_dotenv
from storage import save_raw_data

load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")
client = serpapi.Client(api_key=API_KEY)


def date_validation(date_entered: str) -> str:
        """Validate that the entered date is a real calendar date.

        Ensures the date follows YYYY-MM-DD and rejects impossible dates
        such as 2026-02-45.
        """

        try:
                datetime.strptime(date_entered, "%Y-%m-%d")
                return date_entered
        except ValueError:
                raise ValueError("Enter a valid date in YYYY-MM-DD format.")
        

def get_arguments() -> argparse.Namespace:
        """Define and parse command-line arguments for the flight search.

        Requires origin and destination airport codes.
        Defaults to today's date and USD if date and currency aren't provided.
        """

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


def fetch_flights(origin: str, destination: str, outbound_date: str, currency: str) -> dict:
        """Fetch flight search results from Google Flights using SerpApi.

        Returns the raw search results for the specified route, date and currency.
        """
        
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
        # Parse command-line arguments and fetch flight search results.

        args = get_arguments()

        results = fetch_flights(
                args.origin,
                args.destination,
                args.date,
                args.currency
        )

        # Save the results, skipping the run if duplicate data already exists.
        saved = save_raw_data(results)

        if saved:
                print("flight data saved successfully")
                print(results)
        else:
                print("Flight data already exists. Nothing was saved.")