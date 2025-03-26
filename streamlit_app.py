import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Initialize database
def init_db():
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parking
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  vehicle_number TEXT UNIQUE NOT NULL,
                  vehicle_type TEXT NOT NULL,
                  entry_time TIMESTAMP NOT NULL)''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Set page config
st.set_page_config(
    page_title="Smart Car Parking System",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        margin-top: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🚗 Smart Car Parking System")

# Create three columns for the main interface
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Park Vehicle")
    with st.form("park_form"):
        vehicle_number = st.text_input("Vehicle Number")
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck", "Bus"])
        park_submit = st.form_submit_button("Park Vehicle")
        
        if park_submit:
            if vehicle_number:
                try:
                    conn = sqlite3.connect('parking.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO parking (vehicle_number, vehicle_type, entry_time) VALUES (?, ?, ?)",
                             (vehicle_number, vehicle_type, datetime.now()))
                    conn.commit()
                    conn.close()
                    st.success("Vehicle parked successfully!")
                except sqlite3.IntegrityError:
                    st.error("Vehicle already parked!")
            else:
                st.error("Please enter a vehicle number")

with col2:
    st.subheader("Exit Vehicle")
    with st.form("exit_form"):
        exit_vehicle_number = st.text_input("Vehicle Number to Exit")
        exit_submit = st.form_submit_button("Exit Vehicle")
        
        if exit_submit:
            if exit_vehicle_number:
                conn = sqlite3.connect('parking.db')
                c = conn.cursor()
                c.execute("DELETE FROM parking WHERE vehicle_number = ?", (exit_vehicle_number,))
                if c.rowcount > 0:
                    conn.commit()
                    st.success("Vehicle exited successfully!")
                else:
                    st.error("Vehicle not found!")
                conn.close()
            else:
                st.error("Please enter a vehicle number")

with col3:
    st.subheader("Parking Status")
    conn = sqlite3.connect('parking.db')
    df = pd.read_sql_query("SELECT * FROM parking", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df)
        st.metric("Total Vehicles", len(df))
    else:
        st.info("No vehicles currently parked")
        st.metric("Total Vehicles", 0)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Name") 