import pandas as pd

aca_urls = [
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton%20McCauley.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/St.%20Albert.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Woodcroft.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton%20East.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton%20Lendrum.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Ardrossan.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Sherwood%20Park.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/O%E2%80%99Morrow%20Station%201.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Poacher%E2%80%99s%20Landing%20Station%202.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Leduc%20Sensor.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Enoch.csv"
]

wcas_urls = [
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Breton.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Carrot_Creek.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Drayton_Valley.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Edson.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Genesee.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Hinton-Drinnan.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Meadows.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Powers.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Steeper.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Wagner2.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Hinton-Hillcrest.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/WCAS/Jasper.csv"
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

