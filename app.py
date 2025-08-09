import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import os
import plotly.express as px

st.set_page_config(page_title="IT Support Portal", layout="wide")
st.title("🛠 Internal IT Support Request Portal")

# -- Sidebar navigation
page = st.sidebar.radio("Navigate", ["Submit Ticket", "Admin Dashboard"])

# -- File setup
DATA_FILE = "tickets.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Ticket ID", "Name", "Department", "Request Type", "Urgency", "Description", "Status", "Submitted At", "Assigned To"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -- Ticket submission page
if page == "Submit Ticket":
    st.subheader("Submit a New Request")

    name = st.text_input("Name")
    department = st.selectbox("Department", ["HR", "Engineering", "Sales", "Finance"])
    request_type = st.selectbox("Request Type", ["Password Reset", "Software Access", "Hardware Issue", "Other"])
    urgency = st.selectbox("Urgency", ["Low", "Medium", "High"])
    description = st.text_area("Describe your issue")

    if st.button("Submit Request"):
        ticket_id = str(uuid.uuid4())[:8].upper()
        submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        status = "Open"
        tech_assigned = "Alex"

        new_ticket = {
            "Ticket ID": ticket_id,
            "Name": name,
            "Department": department,
            "Request Type": request_type,
            "Urgency": urgency,
            "Description": description,
            "Status": status,
            "Submitted At": submitted_at,
            "Assigned To": tech_assigned
        }

        df = load_data()
        df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
        save_data(df)

        st.success(f"✅ Ticket {ticket_id} submitted! Assigned to {tech_assigned}.")

# -- Admin dashboard
elif page == "Admin Dashboard":
    st.subheader("📊 Admin Dashboard – IT Ticket Analytics")
    df = load_data()

    if df.empty:
        st.warning("No tickets submitted yet.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Tickets", len(df))
            st.metric("Open Tickets", len(df[df["Status"] == "Open"]))

        with col2:
            urgent_count = len(df[df["Urgency"] == "High"])
            st.metric("High Urgency Tickets", urgent_count)
            assigned_agents = df["Assigned To"].nunique()
            st.metric("Support Agents", assigned_agents)

        st.markdown("### Tickets by Request Type")
        fig = px.histogram(df, x="Request Type", color="Urgency", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Tickets by Department")
        fig2 = px.pie(df, names="Department", title="Department Distribution")
        st.plotly_chart(fig2, use_contai
