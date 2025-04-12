#main.py

import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
import uuid

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from explain import get_score_plot
from detect import detect_anomaly, profile_user

#from model.explain import get_shap_plot
#from model.detect import detect_anomaly, profile_user

# Load historical data
df = pd.read_csv("data/simulated_upi_transactions.csv")  # ya jo bhi tera data source hai

st.title("🔍 UPI Fraud Detection - Real Time")

# User Input Fields
with st.form("txn_form"):
    st.subheader("🔐 Enter Transaction Details")
    transaction_id = str(uuid.uuid4())

    user_id = st.selectbox("Select User", (df['user_id'].unique()))
    device_id = st.selectbox("Select Device", (df['device_id'].unique()))

    amount = st.number_input("Amount (₹)", min_value=0)
    location = st.selectbox("Select Location", (df['location'].unique()))

    #device_id = st.text_input("Device ID")
    merchant_category=st.selectbox("Select merchant category", (df['merchant_category'].unique()))
    submitted = st.form_submit_button("Submit Transaction")

if submitted:
    # Create row from user input
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = pd.Series({
        'transaction_id': transaction_id,
        'user_id': user_id,
        'amount': amount,
        'location': location,
        'device_id': device_id,
        'timestamp' : timestamp,
        'merchant_category' : merchant_category
    })

    st.write(f"User: {user_id} | Amount: ₹{amount} | Location: {location} | Device: {device_id} | Timestamp: {timestamp}")

    # Profile user based on existing data
    user_profiles = profile_user(df)

    # Detect anomaly
    flag = detect_anomaly(row, user_profiles)

    if flag:
        st.error("⚠️ Anomaly Detected!")
        try:
            fig = get_score_plot(row,df)
            if fig:
                st.pyplot(fig)
            else:
                st.warning("Score Visualisation plot not available for this transaction.")
        except Exception as e:
            st.error(f"Error generating plot: {e}")
            
        st.error("Triggering OTP verification.....")
        generated_otp = random.randint(1000, 9999)
        # st.warning(f"Generated OTP: {generated_otp}")  # Remove in prod
        st.caption("🔐 OTP sent to your registered device.")


        otp = st.text_input("Enter OTP to proceed", type="password")
        if otp:
            if otp == str(generated_otp):
                st.success("✅ OTP Verified.")
            else:
                st.error("❌ Incorrect OTP.")
                # st.pyplot(get_shap_plot(row))
                

    else:
        st.success("✅ Transaction looks normal.")
