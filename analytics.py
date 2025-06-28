import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from textblob import TextBlob

def mood_analytics():
    st.subheader("📊 Mood Analytics")

    # Connect to database and get journal entries
    conn = sqlite3.connect('db.sqlite')
    df = pd.read_sql_query("SELECT * FROM journal", conn)
    
    if df.empty:
        st.warning("No journal entries found. Write some entries to see analytics!")
        return

    # Add sentiment analysis
    df['polarity'] = df['entry'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Add sentiment pie chart
    fig = px.pie(
        df, 
        names=pd.cut(df['polarity'], 
        bins=[-1, -0.2, 0.2, 1], 
        labels=["Negative", "Neutral", "Positive"])
    )
    st.plotly_chart(fig)

    # Add word cloud
    if not df['entry'].empty:
        text = ' '.join(df['entry'])
        wordcloud = WordCloud(width=800, height=400).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    
    # Add conversation analysis if available
    if "messages" in st.session_state and st.session_state.messages:
        st.markdown("### 💭 Conversation Analysis")
        
        # Calculate overall mood from chat history
        chat_sentiments = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                sentiment = TextBlob(msg["content"]).sentiment.polarity
                chat_sentiments.append(sentiment)
        
        if chat_sentiments:
            fig = px.line(
                x=range(len(chat_sentiments)), 
                y=chat_sentiments,
                title="Mood Progression During Conversation",
                labels={"x": "Message Number", "y": "Sentiment"}
            )
            st.plotly_chart(fig)

    conn.close()
