# libraries
import streamlit as st
import pandas as pd

st.title("📂 Upload Dataset")
# Dropdown to select file format
file_format = st.selectbox(
    "Select file format to upload",
    ["Select format", "CSV", "Excel"]
)

# Decide allowed file types
file_types = []
if file_format == "CSV":
    file_types = ["csv"]
elif file_format == "Excel":
    file_types = ["xlsx"]
file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

# Check if file is uploaded
if file is not None:
    # Detect file type
    if file.name.endswith(".csv"):
        df = pd.read_csv(file,encoding="utf-8",keep_default_na=False)
    else:
        df = pd.read_excel(file,encoding="utf-8",keep_default_na=False,)

    # Store in session state
    st.session_state["raw_data"] = df.copy()
    st.session_state["data"] = df.copy()

    st.success("File uploaded successfully")
    st.dataframe(df.head())
else:
    st.info("Please upload a dataset")




    
