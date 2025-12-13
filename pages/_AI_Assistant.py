import streamlit as st
import pandas as pd
import os
from services.ai_assistant import ask_ai  # make sure the path matches your project

st.set_page_config(page_title="AI Cybersecurity Assistant", layout="wide")
st.title("AI Cybersecurity Assistant")

# -------------------------------
# Load Cybersecurity Incidents CSV
# -------------------------------
CSV_PATH = os.path.join("database", "csv_files", "cyber_incidents.csv")

if not os.path.exists(CSV_PATH):
    st.warning(f"No incident data found at: {CSV_PATH}")
    df = pd.DataFrame(columns=['incident_id', 'category', 'severity', 'status', 'date_reported', 'resolution_time'])
else:
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip()  # remove whitespace
    expected_cols = ['incident_id', 'category', 'severity', 'status', 'date_reported', 'resolution_time']
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing columns in CSV: {missing_cols}")
        st.stop()

# -------------------------------
# Display raw incident data
# -------------------------------
st.subheader("Current Incident Data")
if df.empty:
    st.info("No incidents available.")
else:
    st.dataframe(df, use_container_width=True)

# -------------------------------
# AI Assistant Interface
# -------------------------------
st.subheader("Ask the AI about your incidents")

question = st.text_area(
    "Type your question here:",
    key="ai_question",
    placeholder="e.g., Analyze risks and suggest remediation for open incidents."
)

if st.button("Ask AI", key="btn_ask_ai"):
    if not question.strip():
        st.warning("Please type a question before asking the AI.")
    else:
        # Include the CSV data as context
        context = df.to_string(index=False)

        prompt = f"""
You are a Cybersecurity Analyst AI.
Here is the current incident data:

{context}

The user asks:
{question}

Please provide:
- Risk analysis
- Incident prioritization
- Threat modeling
- Recommendations for remediation
"""

        with st.spinner("Generating AI response..."):
            try:
                answer = ask_ai(prompt)
                st.subheader("AI Response")
                st.write(answer)
            except Exception as e:
                st.error(f"AI error: {e}")
