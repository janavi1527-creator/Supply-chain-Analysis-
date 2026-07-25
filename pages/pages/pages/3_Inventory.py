import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

st.title("📦 Inventory Dashboard")
st.markdown("### Monitor Inventory Performance")

# Sidebar Filter
product = st.sidebar.multiselect(
    "Product Type",
    options=df["Product type"].unique(),
    default=df["Product type"].unique()
)

filtered = df[df["Product type"].isin(product)]

# KPIs
avg_stock = filtered["Stock levels"].mean()
min_stock = filtered["Stock levels"].min()
max_stock = filtered["Stock levels"].max()
avg_lead = filtered["Lead times"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Stock", f"{avg_stock:.1f}")
c2.metric("Minimum Stock", int(min_stock))
c3.metric("Maximum Stock", int(max_stock))
c4.metric("Average Lead Time", f"{avg_lead:.1f} Days")

st.divider()

# Stock by Product Type
stock = (
    filtered.groupby("Product type")["Stock levels"]
    .mean()
    .reset_index()
)

fig = px.bar(
    stock,
    x="Product type",
    y="Stock levels",
    color="Product type",
    title="Average Stock by Product Type"
)

st.plotly_chart(fig, use_container_width=True)

# Stock vs Products Sold
fig = px.scatter(
    filtered,
    x="Stock levels",
    y="Number of products sold",
    color="Product type",
    size="Revenue generated",
    hover_data=["SKU"],
    title="Stock vs Products Sold"
)

st.plotly_chart(fig, use_container_width=True)

# Low Stock Products
st.subheader("⚠ Low Stock Products")

low_stock = filtered[filtered["Stock levels"] < 20]

st.dataframe(
    low_stock[
        [
            "SKU",
            "Product type",
            "Stock levels",
            "Number of products sold"
        ]
    ],
    use_container_width=True
)

st.download_button(
    "Download Inventory Data",
    filtered.to_csv(index=False),
    "inventory.csv",
    "text/csv"
)
