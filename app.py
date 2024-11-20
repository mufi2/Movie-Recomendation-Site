import streamlit as st
import pandas as pd
import requests
import pickle
from sklearn.metrics.pairwise import cosine_similarity


# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Function to recommend movies
def recommend(movie):
    if movie not in movies["original_title"].values:
        return [], []
    movie_index = movies[movies["original_title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:7
    ]

    recommended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters


# Load movies data and similarity matrix

movies = pd.read_pickle("D:\Projects\Movie Recomendation System\Model\movie_list.pkl")
similarity = pd.read_pickle(
    "D:\Projects\Movie Recomendation System\Model\similarity.pkl"
)

# Streamlit app layout
st.title("Movie Recommendation System")

# Using a select box for movie suggestions
movie_list = movies["original_title"].values
selected_movie_name = st.selectbox("Enter a movie name", movie_list)

# Recommend button
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    if names:
        st.write("## Recommended Movies:")
        cols = st.columns(len(names))  # Create a column for each recommended movie
        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], width=120)  # Adjust width to fit your layout
                st.write(names[i])
    else:
        st.subheader("Movie not found.")
