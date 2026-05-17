
import streamlit as st
import psutil
import sqlite3
import pandas as pd
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="NeuroDesk AI",
    page_icon="🧠",
    layout="wide"
)

# DATABASE
conn = sqlite3.connect("neurodesk.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")

conn.commit()

# CUSTOM CSS
st.markdown("""
<style>
body {
    background-color: #07111F;
}

.main {
    background: #07111F;
    color: white;
}

.stApp {
    background: linear-gradient(to bottom right, #07111F, #111827);
}

.card {
    background: #111827;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0,255,255,0.1);
}

.big-text {
    font-size: 40px;
    font-weight: bold;
    color: cyan;
}

.title {
    font-size: 55px;
    font-weight: bold;
    color: #00F5FF;
    text-align: center;
}

.subtitle {
    color: #9CA3AF;
    text-align: center;
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="title">NEURODESK AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Elite Futuristic Productivity Dashboard</div>',
    unsafe_allow_html=True
)

# SIDEBAR
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard",
        "Tasks",
        "Notes",
        "Analytics"
    ]
)

# DASHBOARD
if page == "Dashboard":

    col1, col2 = st.columns(2)

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("CPU Usage")
        st.markdown(
            f'<div class="big-text">{cpu}%</div>',
            unsafe_allow_html=True
        )
        st.progress(int(cpu))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("RAM Usage")
        st.markdown(
            f'<div class="big-text">{ram}%</div>',
            unsafe_allow_html=True
        )
        st.progress(int(ram))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

    st.info(f"Current Time: {current_time}")

# TASK PAGE
elif page == "Tasks":

    st.header("Smart Task Manager")

    task = st.text_input("Enter New Task")

    if st.button("Add Task"):
        if task:
            cursor.execute(
                "INSERT INTO tasks(task, status) VALUES(?, ?)",
                (task, "Pending")
            )
            conn.commit()
            st.success("Task Added Successfully")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    if tasks:

        data = []

        for task in tasks:
            data.append({
                "ID": task[0],
                "Task": task[1],
                "Status": task[2]
            })

        df = pd.DataFrame(data)

        st.dataframe(df, use_container_width=True)

# NOTES PAGE
elif page == "Notes":

    st.header("AI Notes")

    note = st.text_area("Write Your Notes")

    if st.button("Save Note"):
        if note.strip():
            cursor.execute(
                "INSERT INTO notes(content) VALUES(?)",
                (note,)
            )
            conn.commit()
            st.success("Note Saved")

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    st.subheader("Saved Notes")

    for note in notes:
        st.markdown(f"""
        <div class="card">
        {note[1]}
        </div>
        <br>
        """, unsafe_allow_html=True)

# ANALYTICS PAGE
elif page == "Analytics":

    st.header("System Analytics")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CPU", f"{cpu}%")

    with col2:
        st.metric("RAM", f"{ram}%")

    with col3:
        st.metric("Disk", f"{disk}%")

    st.progress(int(cpu))
    st.progress(int(ram))
    st.progress(int(disk))

# FOOTER
st.markdown("---")
st.caption("NeuroDesk AI © 2026 | Premium Python Streamlit Application") 
