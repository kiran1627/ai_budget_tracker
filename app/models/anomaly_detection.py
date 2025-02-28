import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, numeric_columns, contamination=0.03):
    """Apply Isolation Forest for anomaly detection."""
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    df["Anomaly"] = iso_forest.fit_predict(df[numeric_columns])
    df["Anomaly_Flag"] = df["Anomaly"].apply(lambda x: "Fraud" if x == -1 else "Normal")
    
    return df
