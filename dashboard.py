import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Employee Shift Scheduler",
    page_icon="📅",
    layout="wide"
)

employees = [
    "Ali",
    "Ahmed",
    "Saad",
    "Usman",
    "Hamza",
    "Bilal",
    "Zain",
    "Awais"
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

shifts = [
    "Morning",
    "Evening",
    "Night"
]

# -----------------------------
# Header
# -----------------------------

st.title("📅 Employee Shift Scheduler")
st.caption("Optimization using Google OR-Tools")

st.divider()

# -----------------------------
# Statistics
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Employees", len(employees))
col2.metric("Days", len(days))
col3.metric("Shifts", len(shifts))

st.divider()


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙ Settings")

selected_employees = st.sidebar.multiselect(
    "Select Employees",
    employees,
    default=employees
)

st.sidebar.divider()

leave_employee = st.sidebar.selectbox(
    "Employee on Leave",
    selected_employees
)

leave_day = st.sidebar.selectbox(
    "Leave Day",
    days
)

st.sidebar.divider()

preferred_shift = st.sidebar.selectbox(
    "Preferred Shift",
    shifts
)

st.sidebar.divider()

generate = st.sidebar.button(
    "Generate Schedule",
    use_container_width=True
)

st.header("Weekly Schedule")

if os.path.exists("employee_schedule.csv"):

    df = pd.read_csv("employee_schedule.csv")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("Generate a schedule first.")

    st.header("📊 Employee Workload")

workload = (
    df[["Employee 1", "Employee 2"]]
    .stack()
    .value_counts()
    .reset_index()
)

workload.columns = ["Employee", "Shifts"]

st.bar_chart(
    workload.set_index("Employee")
)

with open("employee_schedule.csv", "rb") as f:
    st.download_button(
        "⬇ Download Schedule",
        f,
        file_name="employee_schedule.csv",
        mime="text/csv"
    )

    col1, col2, col3 = st.columns(3)

col1.metric("Total Shift Slots", 21)
col2.metric("Employees Assigned", 42)
col3.metric("Optimization", "Optimal")

st.caption(
    "Built using Python • Google OR-Tools • Constraint Programming • Streamlit"
)

