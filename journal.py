import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

def journal_interface():
    st.subheader("📓 Digital Journal")
    
    # Initialize database connection
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    
    # Create table if it doesn't exist (don't drop existing table)
    c.execute('''CREATE TABLE IF NOT EXISTS journal 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 entry TEXT, 
                 mood TEXT,
                 timestamp TEXT)''')
    conn.commit()
    
    # Sidebar for viewing past entries
    st.sidebar.subheader("📚 Journal History")
    entries = pd.read_sql_query("SELECT * FROM journal ORDER BY timestamp DESC", conn)
    if not entries.empty:
        st.sidebar.success(f"Total Entries: {len(entries)}")
        for _, row in entries.iterrows():
            with st.sidebar.expander(f"📝 {row['timestamp'][:16]}"):
                st.write(f"**Mood:** {row['mood']}")
                st.write(row['entry'])
    else:
        st.sidebar.info("No journal entries yet. Start writing! ✨")
    
    # Main journal interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text = st.text_area("Express your thoughts and feelings...", height=200)
    
    with col2:
        mood = st.selectbox(
            "How are you feeling?",
            ["😊 Happy", "😌 Calm", "😕 Confused", 
             "😢 Sad", "😠 Angry", "😰 Anxious"]
        )
    
    # Save entry
    if st.button("💾 Save Entry"):
        if text.strip():  # Check if entry is not empty
            try:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('INSERT INTO journal (entry, mood, timestamp) VALUES (?, ?, ?)', 
                         (text, mood, now))
                conn.commit()
                st.success("Journal entry saved successfully! 🎉")
                st.experimental_rerun()  # Refresh to show new entry
            except Exception as e:
                st.error(f"Error saving entry: {str(e)}")
        else:
            st.warning("Please write something before saving.")
    
    # Search functionality
    st.markdown("---")
    search_term = st.text_input("🔍 Search your past entries")
    if search_term:
        search_results = pd.read_sql_query(
            "SELECT * FROM journal WHERE entry LIKE ? ORDER BY timestamp DESC",
            conn,
            params=(f"%{search_term}%",)
        )
        if not search_results.empty:
            st.subheader("Search Results")
            for _, row in search_results.iterrows():
                with st.expander(f"📝 Entry from {row['timestamp'][:16]}"):
                    st.write(f"**Mood:** {row['mood']}")
                    st.write(row['entry'])
        else:
            st.info("No entries found matching your search.")
    
    conn.close()
