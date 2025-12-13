import streamlit as st
import pandas as pd
import plotly.express as px

from database.db_manager import DatabaseManager
from database.crud import get_all_datasets
from services.ai_assistant import ask_ai

st.title(" Data Science Dashboard")

# ---------------------------
# AUTH CHECK
# ---------------------------
if "role" not in st.session_state:
    st.session_state.role = None
if st.session_state.role != "data":
    st.error("Access denied: Data role required. Go to login page first.")
    st.stop()

db = DatabaseManager()

# ---------------------------
# LOAD DATASETS USING OOP CRUD
# ---------------------------
datasets = get_all_datasets()
df = pd.DataFrame([vars(d) for d in datasets])

st.subheader(" Dataset Catalog")
st.dataframe(df)

# ---------------------------
# CREATE DATASET
# ---------------------------
st.subheader(" Add New Dataset")

col1, col2 = st.columns(2)

with col1:
    new_name = st.text_input("Dataset Name")
    new_department = st.selectbox("Department", ["Cyber", "Data", "IT"])

with col2:
    new_rows = st.number_input("Number of Rows", min_value=0)
    new_size = st.number_input("File Size (MB)", min_value=0.0)

new_date = st.date_input("Upload Date")

if st.button("Add Dataset"):
    db.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, department, num_rows, file_size_mb, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (new_name, new_department, new_rows, new_size, str(new_date)))

    st.success("Dataset added successfully! Refresh the page.")

# ---------------------------
# UPDATE DATASET SIZE
# ---------------------------
st.subheader(" Update Dataset Size")

dataset_names = [d.name for d in datasets]

dataset_to_update = st.selectbox("Select Dataset", dataset_names)
new_size_update = st.number_input("New File Size (MB)", min_value=0.0)

if st.button("Update Size"):
    db.execute("""
        UPDATE datasets_metadata
        SET file_size_mb=?
        WHERE dataset_name=?
    """, (new_size_update, dataset_to_update))

    st.success("Dataset updated successfully! Refresh the page.")

# ---------------------------
# DELETE DATASET
# ---------------------------
st.subheader(" Delete Dataset")

dataset_to_delete = st.selectbox(
    "Select Dataset to Delete",
    dataset_names,
    key="delete_dataset"
)

if st.button("Delete Dataset"):
    db.execute(
        "DELETE FROM datasets_metadata WHERE dataset_name=?",
        (dataset_to_delete,)
    )
    st.warning("Dataset deleted.")

# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.subheader(" Storage Usage by Department")

fig1 = px.bar(
    df,
    x="department",
    y="size_mb",
    title="Total Dataset Size per Department"
)
st.plotly_chart(fig1)

st.subheader(" Rows per Dataset")

fig2 = px.bar(
    df,
    x="name",
    y="num_rows",
    title="Number of Rows per Dataset"
)
st.plotly_chart(fig2)

# ---------------------------
# AI ASSISTANT
# ---------------------------
st.subheader(" Data Governance AI Assistant")

question = st.text_area("Ask the AI about datasets, storage, or governance:")

if st.button("Ask AI"):
    context = df.to_string()

    prompt = f"""
    You are a Data Governance and Analytics AI.

    Dataset metadata:
    {context}

    User question:
    {question}

    Provide insights on:
    - storage optimization
    - dataset redundancy
    - governance risks
    - archiving recommendations
    """

    response = ask_ai(prompt)
    st.write(response)
