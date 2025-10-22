import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- 0. Configuration & Data Loading ---

st.set_page_config(
    page_title="RFM Customer Segmentation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# @st.cache_data is used to prevent the app from reloading data on every user interaction
@st.cache_data
def load_data():
    """Loads and returns the final segmented data and summary table."""
    try:
        segments_df = pd.read_csv('rfm_customer_segments.csv')
        summary_df = pd.read_csv('rfm_cluster_summary.csv')
        
        # --- Naming and Mapping Update ---
        # Map Cluster_Label (0, 1, 2) to the NEW Strategic Names
        # IMPORTANT: This assumes your K-Means clustering results were:
        # Cluster 0 = High Monetary/High Frequency/Low Recency (Best)
        # Cluster 2 = Mid Monetary/Mid Frequency/Mid Recency (Growing)
        # Cluster 1 = Low Monetary/Low Frequency/High Recency (Hibernating)
        mapping = {
            0: '0 - Best Customers 🏆', 
            2: '2 - Growing Customers 📈', 
            1: '1 - Hibernating Customers 💤'
        }
        summary_df['Strategic Name'] = summary_df['Cluster_Label'].map(mapping)
        segments_df['Strategic Name'] = segments_df['Cluster_Label'].map(mapping)
        
        return segments_df, summary_df
    except FileNotFoundError:
        st.error("Error: Please ensure 'rfm_customer_segments.csv' and 'rfm_cluster_summary.csv' are in the same directory as app.py.")
        return pd.DataFrame(), pd.DataFrame()

# Load the data
rfm_df, cluster_summary = load_data()


# --- 1. Title and KPIs ---

st.title("🛍️ E-commerce Customer Segmentation (UK Market)")
st.markdown("---")

if not rfm_df.empty:
    
    # Calculate KPIs
    total_customers = rfm_df['Customer ID'].nunique()
    total_revenue = rfm_df['Monetary'].sum()
    # Updated KPI for the new 'Best Customers' name
    best_customer_percentage = cluster_summary[cluster_summary['Strategic Name'] == '0 - Best Customers 🏆']['Percentage'].iloc[0]
    
    # Display KPIs in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers (UK)", f"{total_customers:,}")
    col2.metric("Total Revenue", f"£{total_revenue:,.2f}")
    col3.metric("Best Customers Segment Size", f"{best_customer_percentage:.2f}%")
    st.markdown("---")


# --- 2. Segmentation Strategy (Slicer & Text) ---

st.header("🎯 Strategic Action Plan")

# Create Slicer for selecting the segment
segment_choice = st.selectbox(
    "Select a Customer Segment to view its Strategy:",
    options=cluster_summary['Strategic Name'].tolist(),
    index=0 # Default to Best Customers
)

# --- Updated Strategic Roadmap Text with New Names ---
roadmap = {
    '0 - Best Customers 🏆': {
        'Insight': "Highly engaged, driving the majority of revenue with **very recent purchases** and high Monetary value. Their metrics are significantly above the global average.",
        'Strategy': "Retention & Reward. Implement an **exclusive VIP loyalty tier** offering early access to sales and dedicated support. Goal: Maximize Lifetime Value (LTV) and solidify high purchase frequency."
    },
    '2 - Growing Customers 📈': {
        'Insight': "These customers are the largest segment. They are recent buyers but their Frequency is currently moderate. They are **prime candidates for long-term growth**.",
        'Strategy': "Habit Formation & Conversion. Design targeted **email automation campaigns** focused on increasing purchase cadence. Use personalized product recommendations and small incentives to drive the second/third purchase."
    },
    '1 - Hibernating Customers 💤': {
        'Insight': "Highly lapsed (**average of ≈ 1 year since last purchase**) and lowest spending. This segment is costly to market to with the lowest expected return.",
        'Strategy': "Selective Win-Back. Deploy a single, highly aggressive, **last-chance offer** (e.g., 25% off + free shipping) to a fraction of this segment. If they fail to re-engage, tag them as dormant to save marketing budget."
    }
}

# Display selected strategy
st.subheader(segment_choice)
st.write(f"**Insight:** {roadmap[segment_choice]['Insight']}")
st.write(f"**Strategy:** {roadmap[segment_choice]['Strategy']}")

st.markdown("---")

# --- 3. Core Visualizations (Plots) ---

colA, colB = st.columns(2)

# --- 3A. Cluster Size Breakdown (Donut Chart) ---
with colA:
    st.subheader("Segment Size and Revenue Contribution")
    
    fig_pie = px.pie(
        cluster_summary, 
        values='Percentage', 
        names='Strategic Name', 
        title='Percentage of Customer Base by Segment',
        color='Strategic Name',
        hole=0.4
    )
    fig_pie.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 3B. Snake Plot (Mean RFM Comparison) ---
with colB:
    st.subheader("RFM Metrics Comparison (The Snake Plot)")

    # Prepare data for Snake Plot
    snake_df = cluster_summary[['Recency_Mean', 'Frequency_Mean', 'Monetary_Mean', 'Strategic Name']].set_index('Strategic Name')
    global_mean = snake_df.mean()
    normalized_df = snake_df / global_mean
    normalized_df_t = normalized_df.T.reset_index().rename(columns={'index': 'RFM Metric'})

    # Melt data for Plotly line chart
    df_melt = normalized_df_t.melt(id_vars='RFM Metric', var_name='Segment', value_name='Normalized Value')

    fig_snake = px.line(
        df_melt, 
        x='RFM Metric', 
        y='Normalized Value', 
        color='Segment', 
        markers=True,
        title='Normalized RFM Values (1.0 = Average Customer)'
    )
    fig_snake.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Average Customer (1.0)")
    st.plotly_chart(fig_snake, use_container_width=True)


# --- 4. Final Data Table ---

st.header("📊 Cluster Performance Data")
# Use the new strategic name column for display
st.dataframe(
    cluster_summary.sort_values(by='Monetary_Mean', ascending=False),
    column_order=['Strategic Name', 'Recency_Mean', 'Frequency_Mean', 'Monetary_Mean', 'Count', 'Percentage'],
    hide_index=True
)