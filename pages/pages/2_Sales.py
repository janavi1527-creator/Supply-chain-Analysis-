import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

st.title("📈 Sales Dashboard")
st.markdown("### Analyze Sales Performance")

# Sidebar Filters
product = st.sidebar.multiselect(
    "Product Type",
    df["Product type"].unique(),
    default=df["Product type"].unique()
)

filtered = df[df["Product type"].isin(product)]

# KPIs
total_sales = filtered["Number of products sold"].sum()
total_revenue = filtered["Revenue generated"].sum()
avg_price = filtered["Price"].mean()

c1, c2, c3 = st.columns(3)
c1.metric("📦 Products Sold", f"{total_sales:,.0f}")
c2.metric("💰 Revenue", f"${total_revenue:,.0f}")
c3.metric("💵 Avg Price", f"${avg_price:.2f}")

st.divider()

# Revenue by Product Type
revenue = (
    filtered.groupby("Product type")["Revenue generated"]
    .sum()
    .reset_index()
)

fig = px.bar(
    revenue,
    x="Product type",
    y="Revenue generated",
    color="Product type",
    title="Revenue by Product Type"
)
st.plotly_chart(fig, use_container_width=True)

# Revenue by Supplier
supplier = (
    filtered.groupby("Supplier name")["Revenue generated"]
    .sum()
    .reset_index()
)

fig = px.bar(
    supplier,
    x="Supplier name",
    y="Revenue generated",
    color="Supplier name",
    title="Revenue by Supplier"
)
st.plotly_chart(fig, use_container_width=True)

# Sales by Customer Demographics
customer = (
    filtered.groupby("Customer demographics")["Number of products sold"]
    .sum()
    .reset_index()
)

fig = px.pie(
    customer,
    names="Customer demographics",
    values="Number of products sold",
    title="Sales by Customer Demographics"
)
st.plotly_chart(fig, use_container_width=True)

# Top 10 Products
top = (
    filtered.sort_values(
        "Revenue generated",
        ascending=False
    )[["SKU","Product type","Revenue generated"]]
    .head(10)
)

st.subheader("🏆 Top 10 Products")
st.dataframe(top, use_container_width=True)

st.download_button(
    "⬇ Download Sales Data",
    filtered.to_csv(index=False),
    "sales.csv"
)
