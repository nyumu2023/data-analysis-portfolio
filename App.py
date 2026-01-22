#Libraies
import streamlit as st
#=====================End Of section==========================
st.set_page_config(page_title="📊 Data Analysis Dashboard", layout="wide")
st.title("Data Analysis & Visualization Dashboard")
st.write("Use the sidebar to navigate between pages.")
st.sidebar.success("Select a link above 👆")
# Home content
st.header("🏠 Home")
st.markdown(
    """
### Welcome!
This dashboard allows you to:
- Upload datasets (CSV / Excel)
- Clean data interactively
- Visualize data
- Download cleaned datasets
Use the sidebar to navigate.
"""
)