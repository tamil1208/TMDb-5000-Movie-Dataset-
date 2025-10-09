import pandas as pd
import streamlit as st
import pickle
import requests

# Load the movies dataframe
df = pd.read_pickle("movies_data.pkl")
movies_list = df['title'].values

# Load the similarity matrix
with open("similarity_matrix.pkl", "rb") as file:
    similarity = pickle.load(file)

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=834c86e23888276322981ab25f6c2c99&language=en-US'
        )
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    movie_idx = df[df['title'] == movie].index[0]
    sim = similarity[movie_idx]
    sim_movie_list = sorted(list(enumerate(sim)), reverse=True, key=lambda x: x[1])[1:6]

    rec_movie = []
    rec_movie_poster = []
    for mov in sim_movie_list:
        rec_movie.append(df.iloc[mov[0]].title)
        rec_movie_poster.append(fetch_poster(df.iloc[mov[0]].id))

    return rec_movie, rec_movie_poster


# Streamlit UI
st.title("🎬 Movie Recommender System")

movie_name = st.selectbox(
    "Search or select a movie you liked:",
    movies_list
)

if st.button("Recommend"):
    names, posters = recommend(movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

    
    
    
    

