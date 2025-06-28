import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

MOOD_KEYWORDS = {
    "happy": ["happy hindi", "party bollywood", "dance hindi", "upbeat bollywood"],
    "sad": ["sad hindi songs", "emotional bollywood", "heartbreak hindi", "sad love bollywood"],
    "anxious": ["calm hindi", "peaceful bollywood", "meditation hindi", "relaxing bollywood"],
    "neutral": ["popular hindi", "trending bollywood", "classic hindi", "bollywood hits"]
}

def get_spotify_client():
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=st.secrets["SPOTIPY_CLIENT_ID"],
            client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"]
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        st.error(f"Spotify connection error: {str(e)}")
        return None

def search_mood_playlists(sp, mood):
    try:
        keywords = MOOD_KEYWORDS.get(mood, MOOD_KEYWORDS["neutral"])
        search_term = random.choice(keywords)
        
        results = sp.search(search_term, type='playlist', limit=5)
        if results and 'playlists' in results and 'items' in results['playlists']:
            return results['playlists']['items']
        return []
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

def display_spotify_playlist(playlist_id):
    st.components.v1.iframe(
        f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator",
        height=380,
        width=None
    )

def display_playlist_section(sp, current_mood):
    playlists = search_mood_playlists(sp, current_mood)
    
    if not playlists:
        st.warning("No playlists found. Trying with different keywords...")
        # Try another search with different mood
        playlists = search_mood_playlists(sp, "neutral")
    
    for playlist in playlists:
        try:
            if playlist and 'name' in playlist and 'id' in playlist:
                with st.expander(f"🎵 {playlist['name']}"):
                    display_spotify_playlist(playlist['id'])
                    if 'owner' in playlist and 'tracks' in playlist:
                        st.caption(f"By: {playlist['owner'].get('display_name', 'Unknown')} • Tracks: {playlist['tracks'].get('total', 0)}")
        except Exception as e:
            continue

def relax_interface():
    st.subheader("🎵 Relaxation Tools")
    
    current_mood = st.session_state.get("current_mood", "neutral")
    
    sp = get_spotify_client()
    if not sp:
        st.warning("Please check Spotify API configuration")
        return
    
    mood_emoji = {"happy": "😊", "sad": "😢", "anxious": "😰", "neutral": "😐"}
    st.info(f"{mood_emoji.get(current_mood, '😐')} Based on your conversation, here are some {current_mood} playlists for you")
    
    # Display mood-based playlists with error handling
    display_playlist_section(sp, current_mood)
    
    # Manual search section
    st.markdown("---")
    st.subheader("🔍 Search More Playlists")
    search_query = st.text_input("Enter keywords to search:")
    if search_query:
        try:
            results = sp.search(search_query, type='playlist', limit=3)
            if results and 'playlists' in results and 'items' in results['playlists']:
                for playlist in results['playlists']['items']:
                    if playlist and 'name' in playlist and 'id' in playlist:
                        with st.expander(f"🎵 {playlist['name']}"):
                            display_spotify_playlist(playlist['id'])
                            if 'owner' in playlist and 'tracks' in playlist:
                                st.caption(f"By: {playlist['owner'].get('display_name', 'Unknown')} • Tracks: {playlist['tracks'].get('total', 0)}")
        except Exception as e:
            st.error(f"Search error: {str(e)}")
