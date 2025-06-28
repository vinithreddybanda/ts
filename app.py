import streamlit as st
import requests
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
GENIUS_API_TOKEN = os.getenv('GENIUS_API_TOKEN')

st.set_page_config(page_title="Taylor Swift Lyrics Visualizer", layout="centered")
st.title("🎤 Taylor Swift Lyrics Visualizer")
st.write("Enter a Taylor Swift song title to see the lyrics and a word cloud!")

# Function to search for a song and get its Genius song ID
def search_song(song_title):
    base_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    params = {"q": f"Taylor Swift {song_title}"}
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        hits = response.json()['response']['hits']
        if hits:
            return hits[0]['result']['id']
    return None

# Function to get lyrics from Genius song page
def get_lyrics(song_id):
    song_url = f"https://api.genius.com/songs/{song_id}"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    response = requests.get(song_url, headers=headers)
    if response.status_code == 200:
        path = response.json()['response']['song']['path']
        # Scrape lyrics from the song page
        page_url = f"https://genius.com{path}"
        page = requests.get(page_url)
        from bs4 import BeautifulSoup
        html = BeautifulSoup(page.text, "html.parser")
        # Try all possible containers for lyrics
        lyrics = []
        for div in html.find_all("div", class_=lambda x: x and "Lyrics__Container" in x):
            lyrics.append(div.get_text(separator="\n"))
        if not lyrics:
            # Fallback: try old class
            lyrics_div = html.find("div", class_="lyrics")
            if lyrics_div:
                lyrics.append(lyrics_div.get_text(separator="\n"))
        if lyrics:
            return "\n".join(lyrics).strip()
    return None

# Streamlit UI
song_title = st.text_input("Taylor Swift Song Title", "Love Story")
if st.button("Get Lyrics"):
    if not GENIUS_API_TOKEN:
        st.error("Genius API token not set. Please add it to your .env file.")
    else:
        with st.spinner("Fetching lyrics..."):
            song_id = search_song(song_title)
            if song_id:
                lyrics = get_lyrics(song_id)
                if lyrics:
                    st.subheader("Lyrics:")
                    st.text_area("", lyrics, height=300)
                    # Generate word cloud
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.subheader("Word Cloud:")
                    st.pyplot(fig)
                else:
                    st.error("Could not extract lyrics for this song.")
            else:
                st.error("Song not found. Please check the title and try again.")
