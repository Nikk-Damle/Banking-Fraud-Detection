import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Banking & UPI Fraud Detection Dashboard", layout="wide")

st.title("🚨 Indian Banking & UPI Fraud Detection & Risk Analysis Dashboard")
st.markdown("This dashboard provides real-time insights into transaction anomalies, high-risk cities, and fraud risk scores.")

@st.cache_data
def load_data():
    return pd.read_csv('banking_fraud_data_scored.csv')

df = load_data()

st.sidebar.header("Filter Options")
selected_city = st.sidebar.selectbox("Select City", options=['All'] + list(df['Location_City'].unique()))
risk_filter = st.sidebar.slider("Minimum Fraud Risk Score", float(df['Fraud_Risk_Score'].min()), float(df['Fraud_Risk_Score'].max()), float(df['Fraud_Risk_Score'].min()))

filtered_df = df.copy()
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['Location_City'] == selected_city]

filtered_df = filtered_df[filtered_df['Fraud_Risk_Score'] >= risk_filter]

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Total Frauds Detected", int(filtered_df['Is_Fraud'].sum()))
col3.metric("Avg Transaction Amount (₹)", f"₹ {filtered_df['Amount_INR'].mean():,.2f}")

st.subheader("Filtered Transaction Records")
st.dataframe(filtered_df[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Is_Fraud']].head(100))

st.subheader("Fraud Distribution by Location")
fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(data=filtered_df, x='Location_City', hue='Is_Fraud', palette='Set2', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
