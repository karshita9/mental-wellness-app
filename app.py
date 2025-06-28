import streamlit as st
from chatbot import chat_interface
from journal import journal_interface
from analytics import mood_analytics
from relax import relax_interface

st.sidebar.title("Your True Companion")
page = st.sidebar.selectbox("Navigate", ["Chatbot", "Journal", "Relaxation", "Mood Analytics"])

st.title("🧘 Your True Companion")

if page == "Chatbot":
    chat_interface()
elif page == "Journal":
    journal_interface()
elif page == "Relaxation":
    relax_interface()
elif page == "Mood Analytics":
    mood_analytics()
