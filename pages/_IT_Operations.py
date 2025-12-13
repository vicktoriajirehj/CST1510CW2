import streamlit as st
import pandas as pd
import plotly.express as px

from database.db_manager import DatabaseManager
from database.crud import get_all_tickets
from services.ai_assistant import ask_ai

st.title(" IT Operations Dashboard")

# ---------------------------
# AUTH CHECK
# ---------------------------
if "role" not in st.session_state:
    st.session_state.role = None
if st.session_state.role != "it":
    st.error("Access denied: IT role required. Go to login page first.")
    st.stop()

db = DatabaseManager()

# ---------------------------
# LOAD TICKETS USING OOP CRUD
# ---------------------------
tickets = get_all_tickets()
df = pd.DataFrame([vars(t) for t in tickets])

st.subheader(" IT Support Tickets")
st.dataframe(df)

# ---------------------------
# CREATE TICKET
# ---------------------------
st.subheader(" Create New Ticket")

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
    """, (new_ticket_id, new_assigned, new_status,
          new_priority, str(new_created_date), new_resolution_time))

    st.success("Ticket added successfully! Refresh the page.")

# ---------------------------
# UPDATE TICKET STATUS
# ---------------------------
st.subheader(" Update Ticket Status")

ticket_ids = [t.ticket_id for t in tickets]

ticket_to_update = st.selectbox("Select Ticket", ticket_ids)
new_status_update = st.selectbox(
    "New Status",
    ["Open", "In Progress", "Resolved"],
    key="status_update"
)

if st.button("Update Status"):
    db.execute("""
        UPDATE it_tickets
        SET status=?
        WHERE ticket_id=?
    """, (new_status_update, ticket_to_update))

    st.success("Ticket updated successfully! Refresh the page.")

# ---------------------------
# DELETE TICKET
# ---------------------------
st.subheader("🗑 Delete Ticket")

ticket_to_delete = st.selectbox(
    "Select Ticket to Delete",
    ticket_ids,
    key="delete_ticket"
)

if st.button("Delete Ticket"):
    db.execute(
        "DELETE FROM it_tickets WHERE ticket_id=?",
        (ticket_to_delete,)
    )
    st.warning("Ticket deleted.")

# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.subheader(" Ticket Status Distribution")

fig1 = px.pie(
    df,
    names="status",
    title="Tickets by Status"
)
st.plotly_chart(fig1)

st.subheader(" Average Resolution Time per Staff")

avg_df = df.groupby("assigned_to")["resolution_time"].mean().reset_index()

fig2 = px.bar(
    avg_df,
    x="assigned_to",
    y="resolution_time",
    title="Average Resolution Time by Staff"
)
st.plotly_chart(fig2)

# ---------------------------
# AI ASSISTANT
# ---------------------------
st.subheader(" IT Support AI Assistant")

question = st.text_area("Ask the AI about IT performance or tickets:")

if st.button("Ask AI"):
    context = df.to_string()

    prompt = f"""
    You are an IT Service Management AI.

    Ticket data:
    {context}

    User question:
    {question}

    Provide:
    - performance insights
    - staff workload analysis
    - bottleneck detection
    - process improvement recommendations
    """

    answer = ask_ai(prompt)
    st.write(answer)


