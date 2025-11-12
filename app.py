import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key = "8df33e62773cac688464d6bd7dc00d76"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters

st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    'Select your favourite movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    st.subheader("🎥 Recommended Movies:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])






