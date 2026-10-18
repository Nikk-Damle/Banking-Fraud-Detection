import streamlit as st
import pandas as pd

st.title("Banking Fraud Detection Dashboard")
st.write("Welcome! Let's analyze the transaction data.")

# Load dataset
df = pd.read_csv('banking_fraud_data_scored.csv')
st.dataframe(df.head())
