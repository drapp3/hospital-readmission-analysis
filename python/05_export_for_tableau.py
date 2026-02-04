"""
05_export_for_tableau.py
Prepare data for Tableau dashboard.
"""

import pandas as pd

# Load predictions
df = pd.read_csv("data/processed/predictions.csv")

# Load original data to get readable labels back
df_raw = pd.read_csv("data/raw/diabetic_data.csv")

# Add back readable columns
df["age"] = df_raw.loc[df.index, "age"].values
df["gender"] = df_raw.loc[df.index, "gender"].values
df["race"] = df_raw.loc[df.index, "race"].values

# Select columns for Tableau
tableau_cols = [
    "age",
    "gender", 
    "race",
    "time_in_hospital",
    "num_medications",
    "number_inpatient",
    "readmit_probability",
    "risk_tier",
    "readmit_30_actual"
]

df_tableau = df[tableau_cols].copy()

# Rename for clarity
df_tableau = df_tableau.rename(columns={
    "time_in_hospital": "length_of_stay",
    "number_inpatient": "prior_inpatient_visits",
    "readmit_30_actual": "actually_readmitted"
})

df_tableau.to_csv("data/output/tableau_data.csv", index=False)
print(f"Exported {len(df_tableau):,} rows to data/output/tableau_data.csv")
print(f"\nColumns: {df_tableau.columns.tolist()}")