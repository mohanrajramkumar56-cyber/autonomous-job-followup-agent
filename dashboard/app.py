import streamlit as st
import psycopg2
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Job Follow-Up Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Follow-Up Agent")
st.caption("Personal Job Application Tracking Dashboard")

# -----------------------------
# PostgreSQL Connection
# -----------------------------
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 15432,
    "database": "jobagent",
    "user": "jobagent",
    "password": "jobagent_local_password"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# -----------------------------
# Test Database Connection
# -----------------------------
try:
    conn = get_connection()

    st.success("✅ PostgreSQL connected successfully")

    conn.close()

except Exception as e:
    st.error("❌ PostgreSQL connection failed")
    st.code(str(e))
    st.stop()


# -----------------------------
# Load Applications
# -----------------------------
def load_applications():
    conn = get_connection()

    query = """
    SELECT
        id,
        company,
        role,
        recipient_email,
        application_date,
        status,
        followup_count,
        next_followup_at,
        pause_follow_up,
        followup_stopped,
        priority,
        requires_action
    FROM job_applications
    ORDER BY application_date DESC;
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


applications = load_applications()

# -----------------------------
# Basic Dashboard
# -----------------------------
st.subheader("📊 Application Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Applications",
        len(applications)
    )

with col2:
    st.metric(
        "Active Applications",
        len(
            applications[
                applications["status"] == "ACTIVE"
            ]
        )
    )

with col3:
    st.metric(
        "Follow-ups Sent",
        int(
            applications["followup_count"]
            .fillna(0)
            .sum()
        )
    )

with col4:
    st.metric(
        "Requires Action",
        int(
            applications["requires_action"]
            .fillna(False)
            .sum()
        )
    )

st.divider()

st.subheader("📋 Applications")

st.dataframe(
    applications,
    use_container_width=True,
    hide_index=True
)