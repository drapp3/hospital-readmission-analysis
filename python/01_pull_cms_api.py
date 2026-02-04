"""
Pulls hospital quality data from CMS Hospital Compare API.

Note: This data cannot be joined to the UCI patient dataset due to 
anonymized hospital IDs, but demonstrates API integration skills.
In production, this would enrich patient-level analysis with facility characteristics.
"""

import requests
import pandas as pd

url = "https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0"

response = requests.get(url, params={"limit": 1000})

if response.status_code != 200:
    raise Exception(f"API request failed: {response.status_code}")

data = response.json()
df = pd.DataFrame(data["results"])

print(f"Hospitals pulled: {len(df)}")

cols = [
    "facility_id",
    "facility_name",
    "state",
    "hospital_type",
    "hospital_ownership",
    "emergency_services",
    "hospital_overall_rating",
    "count_of_readm_measures_better",
    "count_of_readm_measures_no_different",
    "count_of_readm_measures_worse"
]

df = df[cols]

df["hospital_overall_rating"] = pd.to_numeric(df["hospital_overall_rating"], errors="coerce")
df["emergency_services"] = df["emergency_services"].map({"Yes": True, "No": False})

df.to_csv("data/raw/hospitals.csv", index=False)
print(f"Saved to data/raw/hospitals.csv")