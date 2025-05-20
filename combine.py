import pandas as pd

aca_urls = [
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton_McCauley.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/St._Albert.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Woodcroft.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton_East.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Edmonton_Lendrum.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Ardrossan.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Sherwood_Park.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/OMorrow_Station_1.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Poachers_Landing_Station_2.csv",
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/main/data/ACA/Leduc_Sensor.csv",
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

