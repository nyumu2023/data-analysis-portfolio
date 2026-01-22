import streamlit as st
import pandas as pd
import re

st.title("🧹 Data Cleaning")

# ---------------- CHECK IF DATA EXISTS ----------------
if "data" not in st.session_state:
    st.warning("Please upload a dataset first")
    st.stop()

# Work on a copy
df = st.session_state["data"].copy()

# ---------------- ORIGINAL DATA ----------------
st.subheader("Original Dataset")
st.dataframe(df.head())

# =====================================================
# CLEANING OPTIONS
# =====================================================
st.subheader(" Cleaning Options")

remove_duplicates = st.checkbox("Remove duplicate rows")
fill_missing = st.checkbox("Fill missing values with blanks")
standardize_columns = st.checkbox("Standardize column names (lowercase & underscore)")
remove_special = st.checkbox("Remove special characters from text", value=True)
remove_spaces = st.checkbox("Remove extra spaces from text", value=True)

case_option = st.selectbox(
    "Text case format",
    ["No Change", "Title Case", "UPPER CASE", "lower case"]
)
format_dates = st.checkbox("Standardize date columns")

if format_dates:
    date_format = st.selectbox(
        "Select date format",
        ["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"]
    )


# =====================================================
# APPLY CLEANING
# =====================================================
if st.button("🚀 Apply Cleaning"):
# ---------------- DATE FORMATTING ----------------
 if format_dates:
    for col in df.columns:
        parsed = pd.to_datetime(df[col], errors="coerce")

        if parsed.notna().sum() > 0:
            if date_format == "YYYY-MM-DD":
                df[col] = parsed.dt.strftime("%Y-%m-%d")
            elif date_format == "DD-MM-YYYY":
                df[col] = parsed.dt.strftime("%d-%m-%Y")
            elif date_format == "MM-DD-YYYY":
                df[col] = parsed.dt.strftime("%m-%d-%Y")
    # ---------------- DUPLICATES ----------------
 if remove_duplicates:
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        st.success(f"Removed {before - after} duplicate rows")

    # ---------------- MISSING VALUES ----------------
if fill_missing:
        df = df.fillna("")
        st.success("Missing values replaced with blanks")

    # ---------------- COLUMN STANDARDIZATION ----------------
if standardize_columns:
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ,", "")
            
        )
        st.success("Column names standardized")

    # ---------------- TEXT CLEANING ----------------
text_cols = df.select_dtypes(include="object").columns

for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

        if remove_spaces:
            df[col] = df[col].str.replace(r"\s+", " ", regex=True)

        if remove_special:
            df[col] = df[col].str.replace(r"['_',',']", "", regex=True)

        if case_option == "Title Case":
            df[col] = df[col].str.title()
        elif case_option == "UPPER CASE":
            df[col] = df[col].str.upper()
        elif case_option == "lower case":
            df[col] = df[col].str.lower()
email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

text_cols = df.select_dtypes(include="object").columns

for col in text_cols:
    sample = df[col].dropna().astype(str).head(10)

    # Check if column contains emails
    is_email_col = sample.str.match(email_pattern).sum() > 0

    if is_email_col:
        # Email-safe cleaning
        df[col] = (
            df[col].astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.replace(r"[^a-zA-Z0-9@._\- ]", "", regex=True)
        )
    else:
        # Normal text cleaning
        df[col] = (
            df[col].astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            
        )

    # Save cleaned data
st.session_state["data"] = df
st.success("Dataset cleaned and ready for analysis")

#Sort columns
st.title("Filter Data")

# Assume df already exists (or from st.session_state)
df = st.session_state.get("data")

if df is None:
    st.warning("Please upload a dataset first")
    st.stop()

# Select column to filter
column = st.selectbox("Select column to filter", df.columns)

# Get unique values
unique_values = df[column].dropna().unique()
# Select values
selected_values = st.multiselect(
    f"Select {column} value(s)",
    options=sorted(unique_values)
)

# Apply filter
if selected_values:
    filtered_df = df[df[column].isin(selected_values)]
else:
    filtered_df = df

st.dataframe(filtered_df)
column = st.selectbox("Choose column", df.columns)

if pd.api.types.is_numeric_dtype(df[column]):
    min_val, max_val = st.slider(
        "Select range",
        float(df[column].min()),
        float(df[column].max()),
        (float(df[column].min()), float(df[column].max()))
    )
    filtered_df = df[(df[column] >= min_val) & (df[column] <= max_val)]

elif pd.api.types.is_datetime64_any_dtype(df[column]):
    start_date, end_date = st.date_input(
        "Select date range",
        [df[column].min(), df[column].max()]
    )
    filtered_df = df[
        (df[column] >= pd.to_datetime(start_date)) &
        (df[column] <= pd.to_datetime(end_date))
    ]

else:
    text = st.text_input("Search value")
    filtered_df = df[df[column].astype(str).str.contains(text, case=False, na=False)]
st.subheader("🔄 Smart Data Type Converter")

column = st.selectbox("Select column", df.columns)

current_dtype = df[column].dtype
st.write(f"Current dtype: **{current_dtype}**")

# Determine allowed conversions
if pd.api.types.is_integer_dtype(current_dtype):
    options = ["float", "datetime"]

elif pd.api.types.is_float_dtype(current_dtype):
    options = ["int", "datetime"]

elif pd.api.types.is_object_dtype(current_dtype):
    options = ["int", "datetime"]

elif pd.api.types.is_datetime64_any_dtype(current_dtype):
    options = ["int", "object"]

else:
    options = []

# Show only valid options
if options:
    target_dtype = st.selectbox(
        "Convert to",
        options
    )

    if st.button("Convert Data Type"):
        try:
            if target_dtype == "int":
                df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

            elif target_dtype == "float":
                df[column] = pd.to_numeric(df[column], errors="coerce")

            elif target_dtype == "datetime":
                df[column] = pd.to_datetime(df[column], errors="coerce")

            elif target_dtype == "object":
                df[column] = df[column].astype(str)

            st.success(f"Converted {column} to {target_dtype}")

        except Exception as e:
            st.error(f"Conversion failed: {e}")
else:
    st.warning("No valid conversion options for this column")
st.dataframe(filtered_df)
 # Column selection
st.subheader("❌ Remove Unwanted Columns")
columns_to_delete = st.multiselect(
        "Select columns to delete permanently",
        df.columns.tolist()
    )

if st.button("🗑 Delete Selected Columns"):
        if columns_to_delete:
            df = filtered_df.drop(columns=columns_to_delete)
            st.session_state["data"] = df
            st.success("Selected columns deleted permanently!")
            st.rerun()
        else:
            st.warning("Please select at least one column.")
        st.title("View Records with Dropdown")
st.subheader("✅ Updated Dataset")
st.dataframe(st.session_state["data"].head())
# Create a dropdown to select number of records to display
options = [5, 10, 15, 20,50,100,500,1000]  # you can customize this
num_records = st.selectbox("Select number of records to view", options, index=0)  # default is 5 (index 0)

# Display selected number of records
st.dataframe(filtered_df.head(num_records))

# =====================================================
# CLEANED DATA PREVIEW
# =====================================================
st.subheader("✅ Cleaned Dataset Preview")
st.dataframe(st.session_state["data"].head())
