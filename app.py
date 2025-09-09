import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ----------------- Spotify Helpers -----------------
def get_song_album_cover_url(song_name, artist_name):
    try:
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track", limit=1)

        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            album_cover_url = track["album"]["images"][0]["url"]
            return album_cover_url
    except Exception as e:
        print(f"⚠️ Error fetching album cover for {song_name} - {artist_name}: {e}")

    return "spotify_logo.webp"


def get_audio_features(song_name, artist_name):
    try:
        search_query = f"track:{song_name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track", limit=1)

        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            track_id = track.get("id")

            if track_id:
                features = sp.audio_features([track_id])
                if features and features[0]:  # sometimes returns [None]
                    return features[0]

        return None

    except Exception as e:
        print(f"⚠️ Error fetching audio features for {song_name} - {artist_name}: {e}")
        return None


def get_artist_genres_by_track(name, artist_name):
    """
    Given a track name + artist name, return the artist's genres (list).
    Returns [] on failure.
    """
    try:
        search_query = f"track:{name} artist:{artist_name}"
        results = sp.search(q=search_query, type="track", limit=1)
        if results and results["tracks"]["items"]:
            artist_id = results["tracks"]["items"][0]["artists"][0]["id"]
            artist_info = sp.artist(artist_id)
            return artist_info.get("genres", []) or []
    except Exception as e:
        print(f"⚠️ Error fetching genres for {artist_name}: {e}")
    return []


# ----------------- Recommendation Logic -----------------
def recommend(song):
    """
    Return top-N similar song names and poster urls based on precomputed similarity matrix.
    """
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:21]:  # skip self already, but double-check below
        candidate_song = music.iloc[i[0]].song
        if candidate_song == song:  # extra safeguard
            continue
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(candidate_song, artist))
        recommended_music_names.append(candidate_song)

    return recommended_music_names, recommended_music_posters



def recommend_with_context(song, mood="Any", activity="Any", genre="Any"):
    names, posters = recommend(song)

    filtered_names = []
    filtered_posters = []

    for name, poster in zip(names, posters):
        if name == song:  # avoid recommending input song
            continue

        artist = music[music['song'] == name].iloc[0].artist
        features = get_audio_features(name, artist)
        if not features:
            continue  # skip songs with no audio features

        # ---- Mood filtering ----
        if mood == "Happy" and features.get("valence", 0) < 0.6:
            continue
        if mood == "Sad" and features.get("valence", 1) > 0.4:
            continue
        if mood == "Energetic" and features.get("energy", 0) < 0.6:
            continue
        if mood == "Chill" and features.get("energy", 1) > 0.4:
            continue

        # ---- Activity filtering ----
        if activity == "Workout" and features.get("tempo", 0) < 100:
            continue
        if activity == "Study" and features.get("acousticness", 1) < 0.3:
            continue
        if activity == "Party" and features.get("danceability", 0) < 0.6:
            continue
        if activity == "Relax" and features.get("acousticness", 1) < 0.5:
            continue

        # ---- Genre filtering ----
        if genre != "Any":
            artist_genres = get_artist_genres_by_track(name, artist)
            genre_lower = genre.strip().lower()
            if not any(genre_lower in g.lower() for g in artist_genres):
                continue

        filtered_names.append(name)
        filtered_posters.append(poster)

        if len(filtered_names) == 5:
            break

    # fallback: if too restrictive, return the top 5 unfiltered (still excluding input song)
    if len(filtered_names) < 5:
        for n, p in zip(names, posters):
            if n == song or n in filtered_names:
                continue
            filtered_names.append(n)
            filtered_posters.append(p)
            if len(filtered_names) == 5:
                break

        if len(filtered_names) == 0:
            return names[:5], posters[:5]

    return filtered_names[:5], filtered_posters[:5]



# ----------------- Streamlit UI -----------------
st.set_page_config(
    page_title="Music Recommendation System",
    page_icon="🎵",
    layout="centered"
)

st.header('Music Recommendation System 🎵')

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Context Filters
st.sidebar.header("Context Filters")
mood = st.sidebar.selectbox(
    "Select Mood",
    ["Any", "Happy", "Sad", "Energetic", "Chill"]
)
activity = st.sidebar.selectbox(
    "Select Activity",
    ["Any", "Workout", "Study", "Party", "Relax"]
)
genre = st.sidebar.selectbox(
    "Preferred Genre",
    ["Any", "Pop", "Rock", "Hip-Hop", "Jazz", "Classical", "Electronic", "Country"]
)

# Song Selection
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# Show Recommendations
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend_with_context(
        selected_song, mood=mood, activity=activity, genre=genre
    )

    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            if idx < len(recommended_music_names):
                st.text(recommended_music_names[idx])
                st.image(recommended_music_posters[idx])
            else:
                st.write("---")
