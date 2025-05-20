import pandas as pd

aca_urls = [
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Edmonton McCauley.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/St. Albert.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Woodcroft.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Edmonton East.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Edmonton Lendrum.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Ardrossan.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Sherwood Park.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/O’Morrow Station 1.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Poacher’s Landing Station 2.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Leduc Sensor.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/ACA/Enoch.csv"
]

wcas_urls = [
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Breton.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Carrot Creek.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Drayton Valley.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Edson.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Genesee.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Hinton-Drinnan.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Meadows.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Powers.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Steeper.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Wagner2.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Hinton-Hillcrest.csv",
    "https://github.com/DKevinM/aqhi_pull/blob/main/data/WCAS/Jasper.csv"
]

def combine_csvs(urls, zone_label):
    combined = []
    for url in urls:
        try:
            df = pd.read_csv(url)
            df["Zone"] = zone_label
            df["StationName"] = url.split("/")[-1].replace(".csv", "")
            combined.append(df)
        except Exception as e:
            print(f"Error reading {url}: {e}")
    return pd.concat(combined, ignore_index=True) if combined else pd.DataFrame()


# Combine separately
aca_combined = combine_csvs(aca_urls, "ACA")
wcas_combined = combine_csvs(wcas_urls, "WCAS")

# Save
aca_combined.to_csv("data/ACA_combined.csv", index=False)
wcas_combined.to_csv("data/WCAS_combined.csv", index=False)

