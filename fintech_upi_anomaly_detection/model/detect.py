# model/detect.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor

def profile_user(df):
    return df.groupby("user_id").agg({
        "amount": ["mean", "std"],
        "device_id": pd.Series.mode,
        "location": pd.Series.mode
    })

def detect_anomaly(txn, profiles):
    user_id = txn["user_id"]
    profile = profiles.loc[user_id]

    amount = float(txn["amount"])
    mean_amt = float(profile["amount"]["mean"])
    std_amt = float(profile["amount"]["std"])

    unusual_device = txn["device_id"] != profile["device_id"]["mode"]
    unusual_location = txn["location"] != profile["location"]["mode"]
    out_of_range = amount > mean_amt + 2 * std_amt

    return unusual_device or unusual_location or out_of_range
