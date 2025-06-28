# chatbot.py

import streamlit as st
import requests
import json
from textblob import TextBlob

def analyze_mood(text):
    analysis = TextBlob(text)
    # Get sentiment polarity (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    if polarity <= -0.5:
        return "sad"
    elif polarity <= -0.1:
        return "anxious"
    elif polarity >= 0.5:
        return "happy"
    else:
        return "neutral"

def chat_interface():
    st.subheader("🤖 AI Wellness Companion")
    
    # Check for API key
    if not st.secrets.get("openrouter_api_key"):
        st.error("⚠️ OpenRouter API key not found!")
        st.info("Please add your OpenRouter API key to `.streamlit/secrets.toml`")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        # Analyze mood from user input
        current_mood = analyze_mood(prompt)
        st.session_state.current_mood = current_mood
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare messages including chat history
                    messages = [
                        {"role": "system", "content": "You are a kind and empathetic mental wellness companion. Help users process their emotions and provide supportive responses."},
                        *st.session_state.messages
                    ]
                    
                    # Make API request
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {st.secrets['openrouter_api_key']}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "localhost:8501",
                            "X-Title": "Mental Wellness Companion",
                        },
                        data=json.dumps({
                            "model": "deepseek/deepseek-r1:free",
                            "messages": messages
                        })
                    )
                    
                    # Parse response
                    if response.status_code == 200:
                        assistant_response = response.json()['choices'][0]['message']['content']
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                        st.markdown(assistant_response)
                        
                        # Suggest music based on mood
                        st.markdown("---")
                        st.markdown(f"🎵 *Based on your mood, I've prepared some {current_mood} music for you in the Relaxation section.*")
                        if st.button("Take me to music recommendations"):
                            st.session_state.page = "Relaxation"
                            st.experimental_rerun()
                    else:
                        st.error(f"API Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.info("Please try again or check your API configuration")
