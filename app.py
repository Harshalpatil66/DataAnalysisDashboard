import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------
# Decorator
# ----------------------------------
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        st.sidebar.success(
            f"Loaded in {round(end - start, 4)} sec"
        )

        return result

    return wrapper

# ----------------------------------
# Load Data Function
# ----------------------------------
@timer
def load_data(file):
    return pd.read_csv(file)

# ----------------------------------
# File Upload
# ----------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data("data/sales.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# ----------------------------------
# Data Preparation
# ----------------------------------
df["Total"] = df["Price"] * df["Quantity"]

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("Filter Data")

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

search = st.sidebar.text_input(
    "Search Product"
)

# ----------------------------------
# Category Filter
# ----------------------------------
if category == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Category"] == category].copy()

# ----------------------------------
# Search Filter
# ----------------------------------
if search:
    filtered_df = filtered_df[
        filtered_df["Product"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ----------------------------------
# Dashboard Title
# ----------------------------------
st.title("📊 Sales Dashboard")

# ----------------------------------
# Dataset Summary
# ----------------------------------
st.subheader("Dataset Summary")

if not filtered_df.empty:
    st.dataframe(filtered_df.describe())
else:
    st.warning("No data available.")

# ----------------------------------
# KPI Cards
# ----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{filtered_df['Total'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Products",
        len(filtered_df)
    )

with col3:
    st.metric(
        "Average Price",
        f"₹{filtered_df['Price'].mean():,.2f}"
        if not filtered_df.empty
        else "₹0"
    )

# ----------------------------------
# Top Product
# ----------------------------------
if not filtered_df.empty:

    top_product = filtered_df.loc[
        filtered_df["Total"].idxmax()
    ]

    st.success(
        f"🏆 Top Product: {top_product['Product']} (Revenue ₹{top_product['Total']:,})"
    )

# ----------------------------------
# Data Table
# ----------------------------------
st.subheader("Sales Data")

st.dataframe(filtered_df)

# ----------------------------------
# Download Button
# ----------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)

# ----------------------------------
# Bar Chart
# ----------------------------------
if not filtered_df.empty:

    st.subheader("Category Wise Quantity")

    category_sales = filtered_df.groupby(
    "Category"
    )["Quantity"].sum()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        category_sales.index,
        category_sales.values
    )

    ax.set_title("Category Wise Sales")
    ax.set_xlabel("Category")
    ax.set_ylabel("Quantity Sold")

    st.pyplot(fig)

st.write(category_sales)

# ----------------------------------
# Pie Chart
# ----------------------------------
st.subheader("Category Distribution")

category_sales = (
    filtered_df.groupby("Category")["Quantity"]
    .sum()
)

fig2, ax2 = plt.subplots(figsize=(7, 7))

ax2.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

ax2.axis("equal")

st.pyplot(fig2)

# ----------------------------------
# Revenue Trend
# ----------------------------------
if not filtered_df.empty:

    st.subheader("Revenue Trend")

    st.line_chart(
        filtered_df["Total"]
    )