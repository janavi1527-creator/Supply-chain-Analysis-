import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

# -----------------------
# Title
# -----------------------
st.title("📊 Supply Chain Analytics - Overview")
st.markdown("### Executive Dashboard")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

product = st.sidebar.multiselect(
    "Product Type",
    df["Product type"].unique(),
    default=df["Product type"].unique()
)

supplier = st.sidebar.multiselect(
    "Supplier",
    df["Supplier name"].unique(),
    default=df["Supplier name"].unique()
)

filtered = df[
    (df["Product type"].isin(product)) &
    (df["Supplier name"].isin(supplier))
]

# -----------------------
# KPI Cards
# -----------------------
revenue = filtered["Revenue generated"].sum()
sales = filtered["Number of products sold"].sum()
stock = filtered["Stock levels"].mean()
lead = filtered["Lead times"].mean()
defect = filtered["Defect rates"].mean()
shipping = filtered["Shipping costs"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${revenue:,.0f}")
col2.metric("📦 Products Sold", f"{sales:,.0f}")
col3.metric("🏬 Avg Stock", f"{stock:.1f}")

col4, col5, col6 = st.columns(3)

col4.metric("🚚 Avg Lead Time", f"{lead:.1f} Days")
col5.metric("⚠ Avg Defect Rate", f"{defect:.2f}%")
col6.metric("🚛 Avg Shipping Cost", f"${shipping:.2f}")

st.divider()

# -----------------------
# Revenue Chart
# -----------------------
left, right = st.columns(2)

with left:
    revenue_chart = (
        filtered.groupby("Product type")["Revenue generated"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_chart,
        x="Product type",
        y="Revenue generated",
        color="Product type",
        title="Revenue by Product Type"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    sales_chart = (
        filtered.groupby("Product type")["Number of products sold"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sales_chart,
        names="Product type",
        values="Number of products sold",
        title="Sales Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Shipping Cost
# -----------------------
left, right = st.columns(2)

with left:

    carrier = (
        filtered.groupby("Shipping carriers")["Shipping costs"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        carrier,
        x="Shipping carriers",
        y="Shipping costs",
        color="Shipping carriers",
        title="Shipping Cost by Carrier"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    inspection = (
        filtered["Inspection results"]
        .value_counts()
        .reset_index()
    )

    inspection.columns = ["Inspection", "Count"]

    fig = px.pie(
        inspection,
        names="Inspection",
        values="Count",
        title="Inspection Results"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Stock Levels
# -----------------------
stock_chart = (
    filtered.groupby("Product type")["Stock levels"]
    .mean()
    .reset_index()
)

fig = px.line(
    stock_chart,
    x="Product type",
    y="Stock levels",
    markers=True,
    title="Average Stock Levels"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Data Table
# -----------------------
st.subheader("Dataset")

st.dataframe(filtered, use_container_width=True)

st.download_button(
    "⬇ Download Filtered Data",
    filtered.to_csv(index=False),
    file_name="filtered_supply_chain.csv"
)
