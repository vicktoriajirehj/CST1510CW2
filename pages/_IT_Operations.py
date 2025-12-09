import streamlit as st
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_manager import DatabaseManager
from services.ai_assistant import ask_ai

st.title("IT Operations Dashboard")

# Protect page
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You must login first.")
    st.stop()

db = DatabaseManager()

# ---------------------------
# LOAD DATA
# ---------------------------
data = db.fetch("SELECT * FROM it_tickets")
df = pd.DataFrame(data, columns=[
    "id", "ticket_id", "assigned_to", "status",
    "priority", "created_date", "resolution_time"
])

st.subheader("🎫 IT Ticket Table")
st.dataframe(df)

# ---------------------------
# CREATE TICKET
# ---------------------------
st.subheader("➕ Create Ticket")

col1, col2 = st.columns(2)

with col1:
    new_ticket_id = st.text_input("Ticket ID")
    new_assigned = st.text_input("Assigned To")

with col2:
    new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])

new_created_date = st.date_input("Created Date")
new_resolution_time = st.number_input("Resolution Time (hours)", min_value=0)

if st.button("Add Ticket"):
    db.execute("""
        INSERT INTO it_tickets
        (ticket_id, assigned_to, status, priority, created_date, resolution_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_ticket_id, new_assigned, new_status, new_priority, str(new_created_date), new_resolution_time))

    st.success("Ticket added! Refresh to update.")

# ---------------------------
# UPDATE TICKET STATUS
# ---------------------------
st.subheader("✏️ Update Ticket Status")

ticket_to_update = st.selectbox(
    "Select Ticket",
    df["ticket_id"].tolist()
)

new_status_u = st.selectbox(
    "New Status",
    ["Open", "In Progress", "Resolved"],
    key="ticket_update"
)

if st.button("Update Ticket"):
    db.execute("""
        UPDATE it_tickets
        SET status=?
        WHERE ticket_id=?
    """, (new_status_u, ticket_to_update))
    st.success("Ticket updated! Refresh page.")

# ---------------------------
# DELETE TICKET
# ---------------------------
st.subheader("🗑 Delete Ticket")

ticket_to_delete = st.selectbox(
    "Select Ticket to Delete",
    df["ticket_id"].tolist(),
    key="ticket_delete"
)

if st.button("Delete Ticket"):
    db.execute("DELETE FROM it_tickets WHERE ticket_id=?", (ticket_to_delete,))
    st.warning("Ticket deleted. Refresh page.")

# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.subheader("📊 Tickets by Status")
fig1 = px.pie(df, names="status", title="Ticket Status Distribution")
st.plotly_chart(fig1)

st.subheader("⏳ Average Resolution Time by Staff")
fig2 = px.bar(
    df.groupby("assigned_to")["resolution_time"].mean().reset_index(),
    x="assigned_to",
    y="resolution_time",
    title="Avg Resolution Time per Staff Member"
)
st.plotly_chart(fig2)

# ---------------------------
# AI ASSISTANT
# ---------------------------
st.subheader("🤖 IT Support AI Assistant")

user_question = st.text_area("Ask the AI about IT support:")

if st.button("Ask AI", key="it_ai"):
    context = df.to_string()

    prompt = f"""
    You are an IT Service Desk Analyst AI.

    Ticket data:
    {context}

    User question:
    {user_question}

    Provide:
    - Performance analysis
    - Staff bottleneck detection
    - Process inefficiencies
    - Recommendations to improve resolution times
    """

    answer = ask_ai(prompt)
    st.write(answer)

