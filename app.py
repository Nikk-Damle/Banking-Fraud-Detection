import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Banking & UPI Fraud Risk Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Modern Styling & Title alignment
st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; }
        .sidebar .sidebar-content { background-color: #1e293b; }
        .title-style {
            font-size: 28px;
            font-weight: bold;
            color: #38bdf8;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        h3 { color: #cbd5e1; }
    </style>
""", unsafe_allow_html=True)

# Title with Both Sides Symbols and Single Line Capital Format
st.markdown('<p class="title-style">🚨 INDIAN BANKING & UPI FRAUD DETECTION HUB 🚨</p>', unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #94a3b8;'>Real-time Transaction Analytics, Risk Scoring & City-wise Intelligence</h5>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('banking_fraud_data_scored.csv')

df = load_data()

total_dataset_records = len(df)

# Sidebar Filters - Risk score normalized strictly from 0.0 to 1.0
st.sidebar.header("🎯 Control Panel")
selected_city = st.sidebar.selectbox("Select City", options=['All'] + sorted(list(df['Location_City'].unique())))

min_score = float(df['Fraud_Risk_Score'].min())
max_score = float(df['Fraud_Risk_Score'].max())
risk_filter = st.sidebar.slider("Minimum Fraud Risk Score", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

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

# Display table with mapped Is_Fraud status for better readability (0 = Safe, 1 = Fraud)
display_table = table_df[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Is_Fraud']].copy()
display_table['Status'] = display_table['Is_Fraud'].apply(lambda x: '🚨 Fraud (1)' if x == 1 else '✅ Safe (0)')

st.dataframe(display_table[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Status']], use_container_width=True)

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
