import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Banking & UPI Fraud Risk Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Modern, Clean Look & Styling
st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; }
        .sidebar .sidebar-content { background-color: #1e293b; }
        h1 { color: #38bdf8; font-family: 'Helvetica Neue', sans-serif; }
        h3 { color: #cbd5e1; }
        .metric-card { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 Indian Banking & UPI Fraud Detection Hub")
st.markdown("### Real-time Transaction Analytics, Risk Scoring & City-wise Intelligence")

@st.cache_data
def load_data():
    return pd.read_csv('banking_fraud_data_scored.csv')

df = load_data()

# Total Records in Dataset (e.g. ~50k)
total_dataset_records = len(df)

# Sidebar Filters
st.sidebar.header("🎯 Control Panel")
selected_city = st.sidebar.selectbox("Select City", options=['All'] + sorted(list(df['Location_City'].unique())))
risk_filter = st.sidebar.slider("Minimum Fraud Risk Score", float(df['Fraud_Risk_Score'].min()), float(df['Fraud_Risk_Score'].max()), float(df['Fraud_Risk_Score'].min()))

# Filtering Logic
filtered_df = df.copy()
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['Location_City'] == selected_city]

filtered_df = filtered_df[filtered_df['Fraud_Risk_Score'] >= risk_filter]

# Top Metrics Row
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Dataset Total Records", f"{total_dataset_records:,}")
col2.metric("Filtered Records Displayed", f"{len(filtered_df):,}")
col3.metric("Total Frauds Detected", int(filtered_df['Is_Fraud'].sum()))
col4.metric("Avg Transaction Amount", f"₹ {filtered_df['Amount_INR'].mean():,.2f}")
st.markdown("---")

# Toggle View
show_fraud_only = st.sidebar.checkbox("🔍 Show Only Fraudulent Transactions")

if show_fraud_only:
    table_df = filtered_df[filtered_df['Is_Fraud'] == 1]
    st.subheader(f"⚠️ High-Risk Fraud Transactions List (City: {selected_city}) — Total Found: {len(table_df):,}")
else:
    table_df = filtered_df
    st.subheader(f"📋 Transaction Records Master Table (Showing all {len(table_df):,} records)")

# FIXED: Removed .head(100) so FULL filtered data (up to 50k) displays properly with pagination built into st.dataframe!
st.dataframe(table_df[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Is_Fraud']], use_container_width=True)

st.markdown("---")
st.subheader("📊 City-wise Fraud Distribution Insights")
fig, ax = plt.subplots(figsize=(12, 5))
sns.countplot(data=filtered_df, x='Location_City', hue='Is_Fraud', palette='viridis', ax=ax)
plt.xticks(rotation=45, ha='right')
ax.set_facecolor('#0f172a')
fig.patch.set_facecolor('#0f172a')
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
st.pyplot(fig)
