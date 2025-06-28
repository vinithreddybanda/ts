# Taylor Swift Lyrics Visualizer

A simple Streamlit app to fetch and visualize Taylor Swift song lyrics using the Genius API. Enter a song title, see the lyrics, and view a word cloud.

## How I Did It
- Used Streamlit for the UI
- Used Genius API to search and fetch lyrics
- Scraped lyrics from Genius song pages
- Generated a word cloud with the `wordcloud` library

## Setup & Run
1. Clone this repo
2. Add your Genius API token to `.env` (see example)
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## .env Example
```
GENIUS_API_TOKEN=your_token_here
```

## Deploy
- Push to GitHub
- Deploy on Streamlit Community Cloud (https://streamlit.io/cloud)


