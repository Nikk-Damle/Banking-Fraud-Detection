import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Banking & UPI Fraud Risk Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Modern Styling, Bigger Single-Line Title & Layout Polish
st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; }
        .sidebar .sidebar-content { background-color: #1e293b; }
        .title-container {
            text-align: center;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .title-style {
            font-size: 38px;
            font-weight: 900;
            color: #38bdf8;
            letter-spacing: 1.5px;
            white-space: nowrap;
            display: inline-block;
        }
        .subtitle-style {
            text-align: center;
            color: #94a3b8;
            font-size: 16px;
            margin-bottom: 25px;
        }
        h3 { color: #cbd5e1; }
    </style>
""", unsafe_allow_html=True)

# Title with Bigger Size, Both Sides Symbols and Strict Single Line Format inside a container
st.markdown("""
    <div class="title-container">
        <span class="title-style">🚨 INDIAN BANKING & UPI FRAUD DETECTION HUB 🚨</span>
    </div>
""", unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Real-time Transaction Analytics, Risk Scoring & City-wise Intelligence</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Nikk-Damle/Banking-Fraud-Detection/main/banking_fraud_data_scored.csv"
    data = pd.read_csv(url)
    return data

df = load_data()

# Fixed total records value as requested
total_dataset_records = 50000

# Sidebar Filters
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
    st.subheader(f"⚠️ High-Risk Fraud Transactions List (City: {selected_city})")
else:
    table_df = filtered_df
    st.subheader("📋 Transaction Records Table")

display_table = table_df[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Is_Fraud']].copy()
display_table['Status'] = display_table['Is_Fraud'].apply(lambda x: '🚨 Fraud (1)' if x == 1 else '✅ Safe (0)')

st.dataframe(display_table[['Transaction_ID', 'User_ID', 'Amount_INR', 'Location_City', 'Device_Type', 'Fraud_Risk_Score', 'Status']], use_container_width=True)

st.markdown("---")
st.subheader("📊 City-wise Fraud Distribution Insights (Interactive)")

fig = px.histogram(
    filtered_df, 
    x='Location_City', 
    color='Is_Fraud', 
    barmode='group',
    color_discrete_map={0: '#38bdf8', 1: '#f43f5e'},
    labels={'Is_Fraud': 'Transaction Status (0=Safe, 1=Fraud)', 'Location_City': 'City', 'count': 'Transaction Count'}
)

fig.update_layout(
    plot_bgcolor='#0f172a',
    paper_bgcolor='#0f172a',
    font_color='#f8fafc',
    xaxis=dict(title='City', gridcolor='#1e293b'),
    yaxis=dict(title='Transaction Count', gridcolor='#1e293b'),
    legend=dict(title='Status', bgcolor='#1e293b', bordercolor='#334155'),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)
