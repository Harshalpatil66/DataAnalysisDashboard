import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Universal Data Analysis Dashboard",
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
# Load Data
# ----------------------------------
@timer
def load_data(file):
    return pd.read_csv(file)

# ----------------------------------
# Sidebar Upload
# ----------------------------------
st.sidebar.title("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    st.title("📊 Universal Data Analysis Dashboard")
    st.info("Please upload a CSV file from the sidebar.")
    st.stop()

# ----------------------------------
# Data Cleaning
# ----------------------------------
df.columns = df.columns.str.strip()

# ----------------------------------
# Dashboard Title
# ----------------------------------
st.title("📊 Universal Data Analysis Dashboard")

# ----------------------------------
# Dataset Preview
# ----------------------------------
st.subheader("Dataset Preview")

st.dataframe(df.head())

# ----------------------------------
# Dataset Information
# ----------------------------------
st.subheader("Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

st.write("### Column Names")
st.write(list(df.columns))

# ----------------------------------
# Missing Values
# ----------------------------------
st.subheader("Missing Values Analysis")

missing_values = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

st.dataframe(missing_values)

# ----------------------------------
# Statistical Summary
# ----------------------------------
st.subheader("Statistical Summary")

numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:
    st.dataframe(numeric_df.describe())
else:
    st.warning("No numeric columns available for statistical analysis.")

# ----------------------------------
# Numeric Column Selection
# ----------------------------------
numeric_columns = df.select_dtypes(
    include=["number"]
).columns

if len(numeric_columns) > 0:

    selected_column = st.selectbox(
        "Select Numeric Column for Analysis",
        numeric_columns
    )

    # ----------------------------------
    # KPI Cards
    # ----------------------------------
    st.subheader("Quick Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Mean",
            round(df[selected_column].mean(), 2)
        )

    with col2:
        st.metric(
            "Maximum",
            round(df[selected_column].max(), 2)
        )

    with col3:
        st.metric(
            "Minimum",
            round(df[selected_column].min(), 2)
        )

    # ----------------------------------
    # Bar Chart
    # ----------------------------------
    st.subheader("Bar Chart")

    st.bar_chart(df[selected_column])

    # ----------------------------------
    # Line Chart
    # ----------------------------------
    st.subheader("Line Chart")

    st.line_chart(df[selected_column])

    # ----------------------------------
    # Histogram
    # ----------------------------------
    st.subheader("Distribution Histogram")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(
        df[selected_column].dropna(),
        bins=10
    )

    ax.set_title(
        f"Distribution of {selected_column}"
    )

    st.pyplot(fig)

else:
    st.warning(
        "No numeric columns found in the uploaded dataset."
    )

# ----------------------------------
# Pie Chart
# ----------------------------------
st.subheader("Pie Chart")

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

if len(categorical_columns) > 0:

    selected_category = st.selectbox(
        "Select Categorical Column",
        categorical_columns
    )

    pie_data = (
        df[selected_category]
        .value_counts()
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    ax2.pie(
        pie_data.values,
        labels=pie_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.axis("equal")

    st.pyplot(fig2)

else:
    st.info(
        "No categorical columns available for pie chart."
    )

# ----------------------------------
# Full Dataset
# ----------------------------------
st.subheader("Complete Dataset")

st.dataframe(df)

# ----------------------------------
# Download Dataset
# ----------------------------------
csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="processed_data.csv",
    mime="text/csv"
)