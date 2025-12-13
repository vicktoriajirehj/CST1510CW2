import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

st.title("Cybersecurity Incidents Dashboard")

# ---------------------------
# AUTH CHECK
# ---------------------------
if "role" not in st.session_state:
    st.session_state.role = None
if st.session_state.role != "cyber":
    st.error("Access denied: cyber role required. Go to login page first")
    st.stop()

# -------------------------------
# Load CSV safely
# -------------------------------
CSV_PATH = os.path.join("database", "csv_files", "cyber_incidents.csv")

if not os.path.exists(CSV_PATH):
    st.error(f"CSV file not found: {CSV_PATH}")
    st.stop()

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()  # remove whitespace

# Ensure expected columns exist
expected_cols = ['incident_id', 'category', 'severity', 'status', 'date_reported', 'resolution_time']
missing_cols = [col for col in expected_cols if col not in df.columns]
if missing_cols:
    st.error(f"Missing columns in CSV: {missing_cols}")
    st.stop()

# -------------------------------
# CRUD OPERATIONS
# -------------------------------
st.subheader("Manage Incidents")

# ADD INCIDENT
st.markdown("### Add New Incident")
col1, col2 = st.columns(2)

with col1:
    new_incident_id = st.text_input("Incident ID", key="new_inc_id")
    new_category = st.text_input("Category", key="new_category")
    new_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"], key="new_severity")

with col2:
    new_status = st.selectbox("Status", ["Open", "Investigating", "Resolved"], key="new_status")
    new_resolution = st.number_input("Resolution Time (Hours)", min_value=0, key="new_resolution")

date_reported = st.date_input("Date Reported", key="new_date")

if st.button("Add Incident", key="btn_add_incident"):
    if new_incident_id.strip() == "":
        st.error("Incident ID cannot be empty!")
    else:
        new_row = {
            "incident_id": new_incident_id,
            "category": new_category,
            "severity": new_severity,
            "status": new_status,
            "date_reported": str(date_reported),
            "resolution_time": new_resolution
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        st.success("Incident added successfully!")
        st.experimental_rerun()  # reload page to refresh data

# UPDATE INCIDENT STATUS
st.markdown("### Update Incident Status")
incident_ids = df["incident_id"].tolist()

incident_to_update = st.selectbox("Select Incident", incident_ids, key="update_incident")
new_status_update = st.selectbox("New Status", ["Open", "Investigating", "Resolved"], key="update_status")

if st.button("Update Status", key="btn_update_status"):
    df.loc[df["incident_id"] == incident_to_update, "status"] = new_status_update
    df.to_csv(CSV_PATH, index=False)
    st.success("Incident status updated!")
    st.experimental_rerun()

# DELETE INCIDENT
st.markdown("### Delete Incident")
incident_to_delete = st.selectbox("Select Incident to Delete", incident_ids, key="delete_incident")

if st.button("Delete Incident", key="btn_delete_incident"):
    df = df[df["incident_id"] != incident_to_delete]
    df.to_csv(CSV_PATH, index=False)
    st.warning("Incident deleted!")
    st.experimental_rerun()

# -------------------------------
# Overview metrics
# -------------------------------
st.subheader("Overview Metrics")
total_incidents = len(df)
open_incidents = len(df[df['status'].str.lower() == 'open'])
resolved_incidents = len(df[df['status'].str.lower() == 'resolved'])

col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", total_incidents)
col2.metric("Open Incidents", open_incidents)
col3.metric("Resolved Incidents", resolved_incidents)

# -------------------------------
# Severity histogram
# -------------------------------
st.subheader("Incidents by Severity")
fig_severity = px.histogram(
    df, x="severity", color="severity",
    title="Incidents by Severity",
    category_orders={"severity": ["Low", "Medium", "High", "Critical"]}
)
st.plotly_chart(fig_severity, use_container_width=True, key="severity_histogram")

# -------------------------------
# Status histogram
# -------------------------------
st.subheader("Incidents by Status")
fig_status = px.histogram(
    df, x="status", color="status",
    title="Incidents by Status"
)
st.plotly_chart(fig_status, use_container_width=True, key="status_histogram")

# -------------------------------
# Category histogram
# -------------------------------
st.subheader("Incidents by Category")
fig_category = px.histogram(
    df, x="category", color="category",
    title="Incidents by Category"
)
st.plotly_chart(fig_category, use_container_width=True, key="category_histogram")

# -------------------------------
# Resolution time chart
# -------------------------------
st.subheader("Resolution Time Distribution (hours)")
fig_resolution = px.histogram(
    df, x="resolution_time",
    nbins=20,
    title="Resolution Time Distribution"
)
st.plotly_chart(fig_resolution, use_container_width=True, key="resolution_histogram")

# -------------------------------
# Optional: display raw data
# -------------------------------
st.subheader("Raw Incident Data")
st.dataframe(df, use_container_width=True)

st.subheader("AI Cybersecurity Assistant")

question = st.text_area("Ask the AI about your security incidents:")

if st.button("Ask AI"):
    context = df.to_string()

    prompt = f"""
    You are a Cybersecurity Analyst AI.
    Here is the incident data:

    {context}

    The user asks:
    {question}

    Provide:
    - Risk analysis
    - Incident prioritization
    - Threat modeling
    - Recommendations for remediation
    """

    answer = ask_ai(prompt)
    st.write(answer)