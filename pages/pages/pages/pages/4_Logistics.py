import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

st.title("🚚 Logistics Dashboard")
st.markdown("### Analyze Shipping & Transportation")

# Sidebar Filters
carrier = st.sidebar.multiselect(
    "Shipping Carrier",
    df["Shipping carriers"].unique(),
    default=df["Shipping carriers"].unique()
)

mode = st.sidebar.multiselect(
    "Transportation Mode",
    df["Transportation modes"].unique(),
    default=df["Transportation modes"].unique()
)

filtered = df[
    (df["Shipping carriers"].isin(carrier)) &
    (df["Transportation modes"].isin(mode))
]

# KPIs
avg_shipping = filtered["Shipping costs"].mean()
avg_lead = filtered["Lead times"].mean()
avg_transport = filtered["Costs"].mean()

k1, k2, k3 = st.columns(3)

k1.metric("🚛 Avg Shipping Cost", f"${avg_shipping:.2f}")
k2.metric("⏳ Avg Lead Time", f"{avg_lead:.1f} Days")
k3.metric("💰 Avg Transport Cost", f"${avg_transport:.2f}")

st.divider()

# Shipping Cost by Carrier
carrier_cost = (
    filtered.groupby("Shipping carriers")["Shipping costs"]
    .mean()
    .reset_index()
)

fig = px.bar(
    carrier_cost,
    x="Shipping carriers",
    y="Shipping costs",
    color="Shipping carriers",
    title="Average Shipping Cost by Carrier"
)

st.plotly_chart(fig, use_container_width=True)

# Transportation Mode Distribution
mode_count = (
    filtered["Transportation modes"]
    .value_counts()
    .reset_index()
)
mode_count.columns = ["Mode", "Count"]

fig = px.pie(
    mode_count,
    names="Mode",
    values="Count",
    title="Transportation Mode Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Lead Time vs Shipping Time
fig = px.scatter(
    filtered,
    x="Lead times",
    y="Shipping times",
    color="Transportation modes",
    size="Shipping costs",
    hover_data=["SKU"],
    title="Lead Time vs Shipping Time"
)

st.plotly_chart(fig, use_container_width=True)

# Route Analysis
route = (
    filtered.groupby("Routes")["Costs"]
    .mean()
    .reset_index()
)

fig = px.bar(
    route,
    x="Routes",
    y="Costs",
    color="Routes",
    title="Average Cost by Route"
)

st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Logistics Data")
st.dataframe(
    filtered[
        [
            "SKU",
            "Shipping carriers",
            "Transportation modes",
            "Lead times",
            "Shipping times",
            "Shipping costs",
            "Routes"
        ]
    ],
    use_container_width=True
)

st.download_button(
    "⬇ Download Logistics Data",
    filtered.to_csv(index=False),
    "logistics.csv",
    "text/csv"
)
