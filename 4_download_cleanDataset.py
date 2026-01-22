from io import BytesIO
import streamlit as st
import pandas as pd
st.title("📥 Download Cleaned Dataset")
if "visible_df" in st.session_state:
    st.subheader("📊 Dataset View")
    st.dataframe(st.session_state["visible_df"])

# Check if cleaned data exists
if "data" not in st.session_state:
    st.warning("Please upload and clean the dataset first")
    st.stop()

df = st.session_state["data"]

st.subheader("Preview of Cleaned Data")
st.dataframe(df.head())

# ---------------- CSV DOWNLOAD ----------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download as CSV",
    data=csv,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)

# ---------------- EXCEL DOWNLOAD ----------------
buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Cleaned Data")

st.download_button(
    label="⬇️ Download Excel File",
    data=buffer.getvalue(),
    file_name="cleaned_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
