from fetcher import fetch_flights

results = fetch_flights()

best_flights = results.get("best_flights", [])

print(best_flights)