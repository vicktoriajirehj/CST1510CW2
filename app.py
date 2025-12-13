import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    layout="wide"
)

st.title("🌐 Multi-Domain Intelligence Platform")

# --------------------------------
# Intro
# --------------------------------
st.markdown("""
Welcome to the **Multi-Domain Intelligence Platform**.

This application provides centralized intelligence across multiple domains:

- 🔒 **Cybersecurity** – incident tracking, risk analysis, AI insights  
- 💻 **IT Operations** – ticket management and operational monitoring  
- 📊 **Data Science** – dataset cataloging and analytics insights  

Use the buttons below to access each dashboard.
""")

st.divider()

# --------------------------------
# Overview Metrics (placeholder)
# --------------------------------
st.subheader(" Platform Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Cyber Incidents", 120)
col2.metric("Open Incidents", 30)
col3.metric("High Severity", 20)
col4.metric("IT Tickets", 80)
col5.metric("Datasets", 25)

st.divider()

# --------------------------------
# Navigation Buttons (FIXED)
# --------------------------------
st.subheader(" Navigate to Dashboards")

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("### 🔒 Cybersecurity")
    st.markdown("""
    - Incident CRUD  
    - Severity & status analytics  
    - AI risk assessment  
    """)
    if st.button("Open Cybersecurity Dashboard"):
        st.switch_page("pages/_Cybersecurity.py")

with colB:
    st.markdown("### 💻 IT Operations")
    st.markdown("""
    - Ticket lifecycle management  
    - Status & assignment tracking  
    - Operational metrics  
    """)
    if st.button("Open IT Operations Dashboard"):
        st.switch_page("pages/_IT_Operations.py")

with colC:
    st.markdown("### 📊 Data Science")
    st.markdown("""
    - Dataset metadata  
    - Department analytics  
    - Data growth insights  
    """)
    if st.button("Open Data Science Dashboard"):
        st.switch_page("pages/_Data_Science.py")

st.divider()

# --------------------------------
# Cross-Domain Snapshot
# --------------------------------
st.subheader("📈 Cross-Domain Snapshot")

sample_df = pd.DataFrame({
    "Domain": ["Cybersecurity", "IT Operations", "Data Science"],
    "Items": [120, 80, 25]
})

fig = px.bar(
    sample_df,
    x="Domain",
    y="Items",
    color="Domain",
    title="Items Across Domains"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# User Guidance
# --------------------------------
st.subheader("💡 How to Use This Platform")

st.markdown("""
1. Start on this dashboard for a high-level overview  
2. Navigate to domain dashboards using the buttons above  
3. Perform CRUD operations inside each domain  
4. Use AI assistants for analysis and recommendations  
""")
