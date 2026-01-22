import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Review Cleaned Dataset")

# Check dataset
if "data" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

filtered_df = st.session_state["data"]

# Select columns
#num_col = st.selectbox(
    #"Select numeric column",
   #filtered_df.select_dtypes(include="number").columns
#)
st.dataframe(filtered_df)

numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = filtered_df.select_dtypes(include=['object', 'category']).columns.tolist()

    # =============================
    # MULTI GRAPH SELECTION
    # =============================
selected_graphs = st.multiselect(
        "Select Graph(s) to Display",
        [
            "Line Chart",
            "Bar Chart",
            "Histogram",
            "Scatter Plot",
            "Box Plot",
            "Pie Chart",
            "Correlation Heatmap"
        ]
    )

st.divider()

    # =============================
    # DISPLAY MULTIPLE VISUALS
    # =============================
cols = st.columns(2)
col_index = 0

for graph in selected_graphs:
        with cols[col_index]:

            st.subheader(graph)

            # LINE CHART
            if graph == "Line Chart":
                x = st.selectbox(f"X-axis ({graph})", numeric_cols, key=f"x_{graph}")
                y = st.selectbox(f"Y-axis ({graph})", numeric_cols, key=f"y_{graph}")

                fig, ax = plt.subplots()
                ax.plot(filtered_df[x], filtered_df[y])
                st.pyplot(fig)

            # BAR CHART
            elif graph == "Bar Chart":
                x = st.selectbox(f"Category ({graph})", categorical_cols, key=f"x_{graph}")
                y = st.selectbox(f"Value ({graph})", numeric_cols, key=f"y_{graph}")

                fig, ax = plt.subplots()
                ax.bar(filtered_df[x], filtered_df[y])
                st.pyplot(fig)

            # HISTOGRAM
            elif graph == "Histogram":
                col = st.selectbox(f"Numeric Column ({graph})", numeric_cols, key=f"h_{graph}")

                fig, ax = plt.subplots()
                ax.hist(filtered_df[col])
                st.pyplot(fig)

            # SCATTER
            elif graph == "Scatter Plot":
                x = st.selectbox(f"X-axis ({graph})", numeric_cols, key=f"x_{graph}")
                y = st.selectbox(f"Y-axis ({graph})", numeric_cols, key=f"y_{graph}")

                fig, ax = plt.subplots()
                ax.scatter(filtered_df[x], filtered_df[y])
                st.pyplot(fig)

            # BOX
            elif graph == "Box Plot":
                x = st.selectbox(f"Category ({graph})", categorical_cols, key=f"x_{graph}")
                y = st.selectbox(f"Numeric ({graph})", numeric_cols, key=f"y_{graph}")

                fig, ax = plt.subplots()
                sns.boxplot(x=filtered_df[x], y=filtered_df[y], ax=ax)
                st.pyplot(fig)

            # PIE
            elif graph == "Pie Chart":
                labels = st.selectbox(f"Category ({graph})", categorical_cols, key=f"l_{graph}")
                values = st.selectbox(f"Values ({graph})", numeric_cols, key=f"v_{graph}")

                fig, ax = plt.subplots()

                ax.pie(filtered_df[values], labels=filtered_df[labels], autopct='%1.1f%%')
                st.pyplot(fig)

            # CORRELATION
            elif graph == "Correlation Heatmap":
                corr = filtered_df[numeric_cols].corr()

                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, ax=ax)
                st.pyplot(fig)

        col_index = (col_index + 1) % 2
 