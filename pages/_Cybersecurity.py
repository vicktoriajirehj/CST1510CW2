import streamlit as st
import pandas as pd
from database.db_manager import DatabaseManager
import plotly.express as px
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()
st.title("Cybersecurity Dashboard")
#implementing role_based access control
if st.session_state.role != "cyber":
    st.error("You do not have permission to view this dashboard.")
    st.stop()

# Protect page
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()

db = DatabaseManager()

# Load incidents
data = db.fetchall("SELECT * FROM cyber_incidents")
df = pd.DataFrame(data, columns=[
    "id", "incident_id", "category", "severity", "status",
    "date_reported", "resolution_time"
])

st.subheader("Incident Table")
st.dataframe(df)


st.subheader("📈 Incidents by Category")
category_chart = px.bar(df, x="category", title="Incidents per Category")
st.plotly_chart(category_chart)

st.subheader("⏳ Average Resolution Time")
resolution_chart = px.bar(
    df.groupby("category")["resolution_time"].mean().reset_index(),
    x="category",
    y="resolution_time",
    title="Average Resolution Time by Category"
)
st.plotly_chart(resolution_chart)

#Adding CRud forms into the cybersecurity dashboard
st.subheader("➕ Add New Incident")

col1, col2 = st.columns(2)

with col1:
    new_incident_id = st.text_input("Incident ID")
    new_category = st.selectbox("Category", ["Phishing", "Malware", "DDoS", "Unauthorized Access"])

with col2:
    new_severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])

new_date = st.date_input("Date Reported")
new_resolution = st.number_input("Resolution Time (hours)", min_value=0)

if st.button("Add Incident"):
    db.execute("""
        INSERT INTO cyber_incidents 
        (incident_id, category, severity, status, date_reported, resolution_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_incident_id, new_category, new_severity, new_status,
          str(new_date), new_resolution))

    st.success("Incident added! Refresh the page to see it.")

# update incident form
st.subheader(" Update Incident Status")

incident_to_update = st.selectbox(
    "Select Incident to Update",
    df["incident_id"].tolist()
)

new_status_update = st.selectbox(
    "New Status",
    ["Open", "In Progress", "Resolved"]
)

if st.button("Update Status"):
    db.execute("""
        UPDATE cyber_incidents
        SET status=?
        WHERE incident_id=?
    """, (new_status_update, incident_to_update))

    st.success(f"Incident {incident_to_update} updated! Refresh to see changes.")

# delete incident form
st.subheader("🗑 Delete Incident")

incident_to_delete = st.selectbox(
    "Select Incident to Delete",
    df["incident_id"].tolist(),
    key="delete_select"
)

if st.button("Delete Incident"):
    db.execute(
        "DELETE FROM cyber_incidents WHERE incident_id=?",
        (incident_to_delete,)
    )
    st.warning(f"Incident {incident_to_delete} deleted. Refresh to update.")

#implementing status distribution chart
st.subheader("📊 Incident Status Distribution")

status_counts = df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]

fig3 = px.pie(
    status_counts,
    names="status",
    values="count",
    title="Incident Status Distribution"
)
st.plotly_chart(fig3)

from services.ai_assistant import ask_ai

st.subheader("🤖 Cybersecurity AI Assistant")

user_question = st.text_area("Ask the AI about cybersecurity insights:")

if st.button("Ask AI"):
    # Provide context from your data
    context = df.to_string()
    full_prompt = f"""
    You are assisting a cybersecurity analyst.
    Here is the current incident dataset:
    {context}

    The user asks:
    {user_question}

    Provide a meaningful, analytical answer.
    """

    answer = ask_ai(full_prompt)
    st.write(answer)
