"""
03_feature_engineering.py
Create features for modeling.
"""

import pandas as pd

df = pd.read_csv("data/processed/cleaned_data.csv")
print(f"Input: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Prior utilization total
df["prior_visits_total"] = df["number_outpatient"] + df["number_emergency"] + df["number_inpatient"]

# High utilizer flag
df["high_utilizer"] = (df["number_inpatient"] >= 2).astype(int)

# Long stay flag
df["long_stay"] = (df["time_in_hospital"] >= 7).astype(int)

# Many medications flag
df["many_meds"] = (df["num_medications"] >= 15).astype(int)

# Medication changed flag
df["med_changed"] = (df["change"] == "Ch").astype(int)
df = df.drop(columns=["change"])

# On insulin flag
df["on_insulin"] = (df["insulin"] != "No").astype(int)

# Save
df.to_csv("data/processed/features_data.csv", index=False)
print(f"Output: {df.shape[0]:,} rows, {df.shape[1]} columns")