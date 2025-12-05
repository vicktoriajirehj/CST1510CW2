import streamlit as st
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_manager import DatabaseManager
from ai.assistant import ask_ai

st.title("📊 Data Science Dashboard")

# Protect page
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()

db = DatabaseManager()

# ---------------------------
# LOAD DATA
# ---------------------------
data = db.fetch("SELECT * FROM datasets_metadata")
df = pd.DataFrame(data, columns=[
    "id", "dataset_name", "department", "num_rows",
    "file_size_mb", "upload_date"
])

st.subheader("📁 Dataset Catalog")
st.dataframe(df)

# ---------------------------
# ADD NEW DATASET (CREATE)
# ---------------------------
st.subheader("➕ Add New Dataset")

col1, col2 = st.columns(2)

with col1:
    new_dataset_name = st.text_input("Dataset Name")
    new_department = st.selectbox("Department", ["IT", "Cyber", "Data"])

with col2:
    new_num_rows = st.number_input("Number of Rows", min_value=0)
    new_size = st.number_input("File Size (MB)", min_value=0.0)

new_date = st.date_input("Upload Date")

if st.button("Add Dataset"):
    db.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, department, num_rows, file_size_mb, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (new_dataset_name, new_department, new_num_rows, new_size, str(new_date)))

    st.success("Dataset added! Refresh to see changes.")

# ---------------------------
# UPDATE DATASET SIZE (UPDATE)
# ---------------------------
st.subheader("✏️ Update Dataset Size")

dataset_to_update = st.selectbox(
    "Select Dataset",
    df["dataset_name"].tolist()
)

new_dataset_size = st.number_input("New File Size (MB)", min_value=0.0, key="size_update")

if st.button("Update Size"):
    db.execute("""
        UPDATE datasets_metadata
        SET file_size_mb=?
        WHERE dataset_name=?
    """, (new_dataset_size, dataset_to_update))
    st.success("Dataset size updated! Refresh to update.")

# ---------------------------
# DELETE DATASET
# ---------------------------
st.subheader("🗑 Delete Dataset")

dataset_to_delete = st.selectbox(
    "Select Dataset to Delete",
    df["dataset_name"].tolist(),
    key="delete_dataset"
)

if st.button("Delete Dataset"):
    db.execute("DELETE FROM datasets_metadata WHERE dataset_name=?", (dataset_to_delete,))
    st.warning("Dataset deleted. Refresh to update.")

# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.subheader("📈 Dataset Size by Department")
fig1 = px.bar(df, x="department", y="file_size_mb", title="Total Data Storage by Department")
st.plotly_chart(fig1)

st.subheader("📊 Rows per Dataset")
fig2 = px.bar(df, x="dataset_name", y="num_rows", title="Dataset Row Counts")
st.plotly_chart(fig2)

# ---------------------------
# AI ASSISTANT
# ---------------------------
st.subheader("🤖 AI Assistant (Data Governance Advisor)")

question = st.text_area("Ask the AI:")

if st.button("Ask AI", key="data_ai"):
    context = df.to_string()

    prompt = f"""
    You are a Data Governance Assistant.

    Dataset catalog:
    {context}

    User question:
    {question}

    Provide insights about:
    - storage optimization
    - archiving recommendations
    - governance risks
    - resource management
    """

    response = ask_ai(prompt)
    st.write(response)
