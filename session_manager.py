import streamlit as st
from textblob import TextBlob

class SessionManager:
    @staticmethod
    def analyze_conversation(messages):
        # Extract user messages
        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        
        if not user_messages:
            return None
        
        # Analyze sentiment
        combined_text = " ".join(user_messages)
        sentiment = TextBlob(combined_text).sentiment
        
        # Determine emotional state
        if sentiment.polarity < -0.3:
            if sentiment.subjectivity > 0.5:
                return "anxious"
            return "sad"
        elif sentiment.polarity < 0.1:
            return "neutral"
        else:
            if sentiment.subjectivity > 0.6:
                return "excited"
            return "happy"

    @staticmethod
    def get_recommendations(emotional_state):
        recommendations = {
            "sad": {
                "music": "Depression Relief",
                "meditation": "Morning Meditation",
                "nature": "Forest Birds",
                "message": "I notice you're feeling down. Let's try some uplifting activities.",
            },
            "anxious": {
                "music": "Anxiety Calm",
                "meditation": "Breathing Exercise",
                "nature": "Ocean Waves",
                "message": "Let's help you relax and calm those anxious thoughts.",
            },
            "neutral": {
                "music": "Focus & Study",
                "meditation": "5-Minute Quick Calm",
                "nature": "Mountain Stream",
                "message": "How about some calming activities to enhance your mood?",
            },
            "happy": {
                "music": "Stress Relief",
                "meditation": "Morning Meditation",
                "nature": "Forest Birds",
                "message": "Great to see you're feeling good! Let's maintain this positive energy.",
            },
            "excited": {
                "music": "Deep Sleep",
                "meditation": "Breathing Exercise",
                "nature": "Rain Sounds",
                "message": "Let's channel this energy into something meaningful.",
            }
        }
        return recommendations.get(emotional_state, recommendations["neutral"])