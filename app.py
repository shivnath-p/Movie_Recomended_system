import pandas as pd
import streamlit as st
import pickle
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
    return full_path

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id  # Ensure 'id' column exists in movies dataset
        recommended_movie_names.append(movies.iloc[i[0]].original_title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Load similarity and movies data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit App
st.title('Movie Recommendation System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['original_title'].values
)

# Button to display recommendations
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)  # Create 5 columns for displaying recommendations
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            if recommended_movie_posters[idx]:
                st.image(recommended_movie_posters[idx])
            else:
                st.text("Poster not available")
