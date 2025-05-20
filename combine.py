import pandas as pd

# Define known station CSV URLs
station_files = [
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
    
    "https://raw.githubusercontent.com/DKevinM/aqhi_pull/new/main/data/ACA/Edmonton_McCauley.csv",
    "https://raw.githubusercontent.com/youruser/yourrepo/main/data/ACA/Woodcroft.csv",
    "https://raw.githubusercontent.com/youruser/yourrepo/main/data/WCAS/St_Albert.csv",

StationName = c("", "", "", "", "",
                  "", "", "", "", "",
                  "Breton", "Carrot Creek", "Drayton Valley", "Edson", "Genesee", "Hinton-Drinnan", "Meadows", 
                  "Powers", "Steeper", "Wagner2", "Hinton-Hillcrest", "Jasper", "Enoch"),
    
    "https://raw.githubusercontent.com/youruser/yourrepo/main/data/WCAS/Carrot_Creek.csv",
    # Add all 23 here manually or dynamically generate
]

combined = []

for url in station_files:
    try:
        df = pd.read_csv(url)
        df["SourceURL"] = url
        df["Zone"] = "ACA" if "/ACA/" in url else "WCAS"
        df["StationName"] = url.split("/")[-1].replace(".csv", "")
        combined.append(df)
    except Exception as e:
        print(f"Error reading {url}: {e}")

# Combine all into one DataFrame
combined_df = pd.concat(combined, ignore_index=True)
combined_df.dropna(subset=["Value"], inplace=True)

# Save locally or push to GitHub
combined_df.to_csv("combined_station_data.csv", index=False)
print("Combined data saved as combined_station_data.csv")
