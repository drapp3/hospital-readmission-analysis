"""
02_data_cleaning.py
Raw data → cleaned data for modeling.
"""

import pandas as pd

df = pd.read_csv("data/raw/diabetic_data.csv")
print(f"Raw: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Drop columns with too much missing data or not useful
drop_cols = ["weight", "max_glu_serum", "A1Cresult", "payer_code", "encounter_id", "patient_nbr"]
df = df.drop(columns=drop_cols)

# Replace "?" with "Unknown"
for col in ["race", "medical_specialty", "diag_1", "diag_2", "diag_3"]:
    df[col] = df[col].replace("?", "Unknown")

# Create binary target
df["readmit_30"] = (df["readmitted"] == "<30").astype(int)
df = df.drop(columns=["readmitted"])

# Save
df.to_csv("data/processed/cleaned_data.csv", index=False)
print(f"Saved: {df.shape[0]:,} rows, {df.shape[1]} columns")
print(f"Target: {df['readmit_30'].mean()*100:.1f}% positive class")