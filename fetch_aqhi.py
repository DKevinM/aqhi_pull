# fetch_aqhi.py
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

stations = [
    {"StationName": "Edmonton McCauley", "Zone": "ACA"},
    {"StationName": "St. Albert", "Zone": "ACA"},
    {"StationName": "Woodcroft", "Zone": "ACA"},
    {"StationName": "Edmonton East", "Zone": "ACA"},
    {"StationName": "Edmonton Lendrum", "Zone": "ACA"},
    {"StationName": "Ardrossan", "Zone": "ACA"},
    {"StationName": "Sherwood Park", "Zone": "ACA"},
    {"StationName": "O’Morrow Station 1", "Zone": "ACA"},
    {"StationName": "Poacher’s Landing Station 2", "Zone": "ACA"},
    {"StationName": "Leduc Sensor", "Zone": "ACA"},
    {"StationName": "Breton", "Zone": "WCAS"},
    {"StationName": "Carrot Creek", "Zone": "WCAS"},
    {"StationName": "Drayton Valley", "Zone": "WCAS"},
    {"StationName": "Edson", "Zone": "WCAS"},
    {"StationName": "Genesee", "Zone": "WCAS"},
    {"StationName": "Hinton-Drinnan", "Zone": "WCAS"},
    {"StationName": "Meadows", "Zone": "WCAS"},
    {"StationName": "Powers", "Zone": "WCAS"},
    {"StationName": "Steeper", "Zone": "WCAS"},
    {"StationName": "Wagner2", "Zone": "WCAS"},
    {"StationName": "Hinton-Hillcrest", "Zone": "WCAS"},
    {"StationName": "Jasper", "Zone": "WCAS"},
    {"StationName": "Enoch", "Zone": "ACA"},
]

def fetch_data(station, days=7):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S-06:00')

    url = "https://data.environment.alberta.ca/EdwServices/aqhi/odata/StationMeasurements"
    params = {
        "$format": "json",
        "$filter": f"StationName eq '{station}' AND ReadingDate gt {start_str}",
        "$orderby": "ReadingDate desc",
        "$select": "StationName,ParameterName,ReadingDate,Value"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json().get("value", [])
        return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️ Failed to fetch {station}: {e}")
        return pd.DataFrame()

Path("data").mkdir(exist_ok=True)
summary = []

for stn in stations:
    df = fetch_data(stn["StationName"])
    if not df.empty:
        zone_path = Path("data") / stn["Zone"]
        zone_path.mkdir(parents=True, exist_ok=True)
        clean_name = (
            stn["StationName"]
            .replace("’", "")
            .replace("'", "")
            .replace(" ", "_")
        )
        df.to_csv(zone_path / f"{clean_name}.csv", index=False)
        summary.append({
            "StationName": stn["StationName"],
            "Zone": stn["Zone"],
            "LastReading": pd.to_datetime(df["ReadingDate"], errors="coerce").max()
        })

pd.DataFrame(summary).to_csv("data/summary.csv", index=False)
print("AQHI fetch complete")
