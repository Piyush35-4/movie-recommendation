import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movies_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(poster_url)
        
    return recommended_movies,recommended_movies_posters

movies = pd.read_pickle('movies.pkl')
similarity = pd.read_pickle('similarity.pkl')

st.title("Movie Recommendation System")

option = st.selectbox(
    'Select a movie: ',
    movies['title'].values
)
if st.button('Recommend'):
    recommended_movies = recommend(option)
    
    m1, m2, m3,m4,m5 = st.columns(5)

    with m1:
        st.text(recommended_movies[0][0])
        st.image(recommended_movies[1][0])

    with m2:
        st.text(recommended_movies[0][1])
        st.image(recommended_movies[1][1])
    
    with m3:
        st.text(recommended_movies[0][2])
        st.image(recommended_movies[1][2])
        
    with m4:
        st.text(recommended_movies[0][3])
        st.image(recommended_movies[1][3])
        
    with m5:
        st.text(recommended_movies[0][4])    
        st.image(recommended_movies[1][4])
        