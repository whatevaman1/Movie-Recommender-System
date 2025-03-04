import os
import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv

# -------------- ENV SETUP --------------
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not set. Please set it in the .env file.")

# -------------- FETCH DATA FROM TMDB --------------
def fetch_movie_details(movie_id):
    """
    Fetch detailed info about a movie from TMDB.
    Returns a dict including poster, overview, release date, rating, etc.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return {
            'id': movie_id,
            'title': 'N/A',
            'poster': 'https://via.placeholder.com/500x750.png?text=No+Image',
            'overview': 'No overview available',
            'release_date': 'N/A',
            'rating': 'N/A'
        }

    data = response.json()
    poster_path = data.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else 'https://via.placeholder.com/500x750.png?text=No+Image'

    return {
        'id': data.get('id', movie_id),
        'title': data.get('title', 'N/A'),
        'poster': poster_url,
        'overview': data.get('overview', 'No overview available'),
        'release_date': data.get('release_date', 'N/A'),
        'rating': data.get('vote_average', 'N/A')
    }

def fetch_trending_movies():
    """
    Fetch a list of trending movies (weekly) from TMDB.
    """
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get('results', [])

def fetch_top_rated_movies():
    """
    Fetch a list of top-rated movies from TMDB.
    """
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get('results', [])

def search_movies(query):
    """
    Search for movies by title using TMDB.
    """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=en-US&query={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get('results', [])

# -------------- RECOMMENDATION LOGIC --------------
def recommend(movie_title):
    """
    Given a movie title (from local 'movies'), return 5 recommended movies (with TMDB details).
    """
    if movie_title not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

    recommended = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended.append(details)

    return recommended

# -------------- LOAD LOCAL DATA --------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------- STREAMLIT PAGE CONFIG --------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon=":clapper:",
    layout="wide"
)

# -------------- CUSTOM CSS FOR STYLING --------------
st.markdown("""
<style>
/* Container adjustments */
.main .block-container {
    max-width: 1200px;
    margin: 0 auto;
    padding-top: 2rem;
}

/* Dark background and text color */
body {
    background-color: #0c0c0c !important;
    color: #fff !important;
}

/* Hide default Streamlit menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Movie container styling */
.movie-container {
    text-align: center;
    margin-bottom: 20px;
}

/* Poster style with fixed width */
.movie-poster {
    border-radius: 10px;
    width: 180px;
    height: auto;
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}
.movie-poster:hover {
    transform: scale(1.05);
}

/* Title styling with hover effect */
.movie-title {
    font-weight: bold;
    font-size: 1.1rem;
    margin-top: 10px;
    color: #fff;
    transition: color 0.2s ease-in-out;
    cursor: pointer;
}
.movie-title:hover {
    text-decoration: underline;
}

/* Additional movie info styling */
.movie-info {
    font-size: 0.9rem;
    color: #ccc;
    margin-top: 5px;
}

/* Custom styling for the expander content to enforce consistent padding/height */
[data-testid="stExpander"] > div:nth-child(2) {
    min-height: 100px;
    padding: 10px;
}

/* Custom button styling */
div.stButton > button:first-child {
    background-color: #6c63ff;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 0.3rem;
    cursor: pointer;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #5750c5;
}
</style>
""", unsafe_allow_html=True)

# -------------- HELPER: DISPLAY MOVIES IN A GRID --------------
def display_movies_in_grid(movie_list, cols=5):
    """
    Display movie dictionaries in a grid with clickable posters and titles.
    """
    if not movie_list:
        st.warning("No movies to display.")
        return

    for i in range(0, len(movie_list), cols):
        row = st.columns(cols)
        for col, movie_data in zip(row, movie_list[i:i+cols]):
            tmdb_id = movie_data.get('id', '')
            tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}"

            with col:
                st.markdown('<div class="movie-container">', unsafe_allow_html=True)
                # Clickable poster
                st.markdown(
                    f"""
                    <a href="{tmdb_link}" target="_blank">
                        <img src="{movie_data['poster']}" class="movie-poster"/>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                # Clickable title
                st.markdown(
                    f"""
                    <a href="{tmdb_link}" target="_blank" style="text-decoration: none; color: #fff;">
                        <div class="movie-title">{movie_data['title']}</div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                # Release date and rating
                release_date = movie_data.get('release_date', 'N/A')
                if release_date != 'N/A':
                    st.markdown(
                        f"<div class='movie-info'>Release: {release_date}</div>",
                        unsafe_allow_html=True
                    )
                rating = movie_data.get('rating', 'N/A')
                if rating != 'N/A':
                    st.markdown(
                        f"<div class='movie-info'>Rating: {rating}</div>",
                        unsafe_allow_html=True
                    )
                # Expander for the movie overview with consistent padding
                with st.expander("Show More"):
                    overview_text = movie_data.get('overview', 'No overview available')
                    st.write(overview_text)
                st.markdown('</div>', unsafe_allow_html=True)

# -------------- MAIN APP INTERFACE --------------
st.title("🎬 Movie Recommender System")

tabs = st.tabs(["Recommendations", "Search", "Trending", "Top Rated"])

# ---- TAB 1: RECOMMENDATIONS ----
with tabs[0]:
    st.subheader("Get Movie Recommendations")
    selected_movie_name = st.selectbox(
        "Select a movie from our dataset:",
        movies['title'].values
    )
    if st.button('Recommend'):
        recommended = recommend(selected_movie_name)
        if not recommended:
            st.warning("No recommendations found. Try another movie.")
        else:
            display_movies_in_grid(recommended, cols=5)

# ---- TAB 2: SEARCH ----
with tabs[1]:
    st.subheader("Search Movies from TMDB")
    query = st.text_input("Type a movie name to search:")
    if st.button("Search"):
        results = search_movies(query)
        if results:
            movie_list = []
            for item in results:
                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else 'https://via.placeholder.com/500x750.png?text=No+Image'
                movie_list.append({
                    'id': item.get('id'),
                    'title': item.get('title', 'N/A'),
                    'poster': poster_url,
                    'overview': item.get('overview', 'No overview available'),
                    'release_date': item.get('release_date', 'N/A'),
                    'rating': item.get('vote_average', 'N/A')
                })
            display_movies_in_grid(movie_list, cols=5)
        else:
            st.warning("No results found. Try a different query.")

# ---- TAB 3: TRENDING ----
with tabs[2]:
    st.subheader("Trending Movies (This Week)")
    trending_data = fetch_trending_movies()
    if trending_data:
        trending_list = []
        for item in trending_data:
            poster_path = item.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else 'https://via.placeholder.com/500x750.png?text=No+Image'
            trending_list.append({
                'id': item.get('id'),
                'title': item.get('title', 'N/A'),
                'poster': poster_url,
                'overview': item.get('overview', 'No overview available'),
                'release_date': item.get('release_date', 'N/A'),
                'rating': item.get('vote_average', 'N/A')
            })
        display_movies_in_grid(trending_list, cols=5)
    else:
        st.warning("Could not fetch trending movies at the moment.")

# ---- TAB 4: TOP RATED ----
with tabs[3]:
    st.subheader("Top Rated Movies")
    top_rated_data = fetch_top_rated_movies()
    if top_rated_data:
        top_rated_list = []
        for item in top_rated_data:
            poster_path = item.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else 'https://via.placeholder.com/500x750.png?text=No+Image'
            top_rated_list.append({
                'id': item.get('id'),
                'title': item.get('title', 'N/A'),
                'poster': poster_url,
                'overview': item.get('overview', 'No overview available'),
                'release_date': item.get('release_date', 'N/A'),
                'rating': item.get('vote_average', 'N/A')
            })
        display_movies_in_grid(top_rated_list, cols=5)
    else:
        st.warning("Could not fetch top rated movies at the moment.")
