import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Quality Dashboard",
    page_icon="✅",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

st.title("✅ Quality Dashboard")
st.markdown("### Product Quality & Inspection Analysis")

# Sidebar Filter
product = st.sidebar.multiselect(
    "Product Type",
    df["Product type"].unique(),
    default=df["Product type"].unique()
)

filtered = df[df["Product type"].isin(product)]

# KPI Cards
avg_defect = filtered["Defect rates"].mean()
avg_cost = filtered["Manufacturing costs"].mean()
pass_count = (filtered["Inspection results"] == "Pass").sum()
fail_count = (filtered["Inspection results"] == "Fail").sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Avg Defect Rate", f"{avg_defect:.2f}%")
c2.metric("Avg Manufacturing Cost", f"${avg_cost:.2f}")
c3.metric("Passed Inspections", pass_count)
c4.metric("Failed Inspections", fail_count)

st.divider()

# Inspection Results
inspection = (
    filtered["Inspection results"]
    .value_counts()
    .reset_index()
)
inspection.columns = ["Result", "Count"]

fig = px.pie(
    inspection,
    names="Result",
    values="Count",
    title="Inspection Results"
)

st.plotly_chart(fig, use_container_width=True)

# Defect Rate by Product
defect = (
    filtered.groupby("Product type")["Defect rates"]
    .mean()
    .reset_index()
)

fig = px.bar(
    defect,
    x="Product type",
    y="Defect rates",
    color="Product type",
    title="Average Defect Rate by Product Type"
)

st.plotly_chart(fig, use_container_width=True)

# Supplier Quality
supplier = (
    filtered.groupby("Supplier name")["Defect rates"]
    .mean()
    .reset_index()
)

fig = px.bar(
    supplier,
    x="Supplier name",
    y="Defect rates",
    color="Supplier name",
    title="Supplier Quality Comparison"
)

st.plotly_chart(fig, use_container_width=True)

# Manufacturing Cost
cost = (
    filtered.groupby("Product type")["Manufacturing costs"]
    .mean()
    .reset_index()
)

fig = px.line(
    cost,
    x="Product type",
    y="Manufacturing costs",
    markers=True,
    title="Manufacturing Cost by Product Type"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Quality Dataset")

st.dataframe(
    filtered[
        [
            "SKU",
            "Product type",
            "Inspection results",
            "Defect rates",
            "Manufacturing costs",
            "Supplier name"
        ]
    ],
    use_container_width=True
)

st.download_button(
    "⬇ Download Quality Data",
    filtered.to_csv(index=False),
    "quality.csv",
    "text/csv"
)
