"""
04_modeling.py
Train readmission prediction model.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve

df = pd.read_csv("data/processed/features_data.csv")
print(f"Data: {df.shape[0]:,} rows")

# Encode categorical columns
cat_cols = df.select_dtypes(include=["object", "str"]).columns.tolist()
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col].astype(str))

# Split features and target
X = df.drop(columns=["readmit_30"])
y = df["readmit_30"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# Train model
model = RandomForestClassifier(
    n_estimators=100, 
    class_weight="balanced",
    random_state=42, 
    n_jobs=-1
)
model.fit(X_train, y_train)

# Get probabilities
y_prob = model.predict_proba(X_test)[:, 1]

print(f"\nROC-AUC: {roc_auc_score(y_test, y_prob):.3f}")

# Find best threshold using precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)

best_thresh = 0.5
for i, r in enumerate(recall):
    if r < 0.5:
        best_thresh = thresholds[i-1]
        break

print(f"Using threshold: {best_thresh:.3f}")

# Apply custom threshold
y_pred = (y_prob >= best_thresh).astype(int)

print(f"\n{classification_report(y_test, y_pred)}")

# Feature importance
print("\nTop 10 Features:")
importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print(importance.head(10).to_string(index=False))

# Save model
import joblib
joblib.dump(model, "data/processed/model.pkl")
print("\nModel saved to data/processed/model.pkl")

# Create intervention tiers based on probability
df_output = X_test.copy()
df_output["readmit_30_actual"] = y_test.values
df_output["readmit_probability"] = y_prob

def assign_tier(prob):
    if prob >= 0.20:
        return "High"
    elif prob >= 0.12:
        return "Medium"
    else:
        return "Low"

df_output["risk_tier"] = df_output["readmit_probability"].apply(assign_tier)

print("\nRisk Tier Distribution:")
print(df_output["risk_tier"].value_counts())

print("\nReadmission Rate by Tier:")
print(df_output.groupby("risk_tier")["readmit_30_actual"].mean().round(3))

# Save predictions
df_output.to_csv("data/processed/predictions.csv", index=False)
print("\nPredictions saved to data/processed/predictions.csv")