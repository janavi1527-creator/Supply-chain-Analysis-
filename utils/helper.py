import pandas as pd

def load_data():
    return pd.read_csv("supply_chain_data.csv")

def format_currency(value):
    return f"${value:,.2f}"

def calculate_kpis(df):
    return {
        "Revenue": df["Revenue generated"].sum(),
        "Sales": df["Number of products sold"].sum(),
        "Stock": df["Stock levels"].mean(),
        "Defect": df["Defect rates"].mean(),
        "Lead": df["Lead times"].mean(),
    }
