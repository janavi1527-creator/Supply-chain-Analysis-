import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("📦 Supply Chain Dashboard")

product = st.sidebar.multiselect(
    "Select Product Type",
    options=df["Product type"].unique(),
    default=df["Product type"].unique()
)

supplier = st.sidebar.multiselect(
    "Select Supplier",
    options=df["Supplier name"].unique(),
    default=df["Supplier name"].unique()
)

filtered = df[
    (df["Product type"].isin(product)) &
    (df["Supplier name"].isin(supplier))
]

# -------------------------
# KPIs
# -------------------------
total_revenue = filtered["Revenue generated"].sum()
total_sales = filtered["Number of products sold"].sum()
avg_stock = filtered["Stock levels"].mean()
avg_defect = filtered["Defect rates"].mean()

st.title("📊 Supply Chain Analytics Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("📦 Products Sold", f"{total_sales:,.0f}")
c3.metric("🏬 Avg Stock", f"{avg_stock:.1f}")
c4.metric("⚠ Avg Defect Rate", f"{avg_defect:.2f}%")

st.divider()

# -------------------------
# Revenue by Product
# -------------------------
col1, col2 = st.columns(2)

with col1:
    revenue = filtered.groupby("Product type")["Revenue generated"].sum().reset_index()

    fig = px.bar(
        revenue,
        x="Product type",
        y="Revenue generated",
        color="Product type",
        title="Revenue by Product Type"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Inspection Results
# -------------------------
with col2:
    inspect = filtered["Inspection results"].value_counts().reset_index()
    inspect.columns = ["Inspection", "Count"]

    fig = px.pie(
        inspect,
        names="Inspection",
        values="Count",
        title="Inspection Results"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Shipping Cost
# -------------------------
col3, col4 = st.columns(2)

with col3:
    carrier = filtered.groupby("Shipping carriers")["Shipping costs"].mean().reset_index()

    fig = px.bar(
        carrier,
        x="Shipping carriers",
        y="Shipping costs",
        color="Shipping carriers",
        title="Average Shipping Cost"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    transport = filtered["Transportation modes"].value_counts().reset_index()
    transport.columns = ["Mode", "Count"]

    fig = px.pie(
        transport,
        names="Mode",
        values="Count",
        title="Transportation Modes"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Dataset Preview")
st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_supply_chain.csv",
    "text/csv"
)
