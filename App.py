import pickle
import streamlit as st
import requests

st.title('🎬 Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster_and_rating(movie_title):
    api_key = "ea9e4856"  # Replace with your actual OMDb API key
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"
    data = requests.get(url).json()

    poster = data.get("Poster") if data.get("Poster") and data["Poster"] != "N/A" else None
    rating = data.get("imdbRating") if data.get("imdbRating") and data["imdbRating"] != "N/A" else "Not Available"

    return poster, rating

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ratings = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title

        poster, rating = fetch_poster_and_rating(movie_title)
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(poster)
        recommended_movie_ratings.append(rating)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ratings

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Recommend'):
    names, posters, ratings = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            st.markdown(f"⭐ IMDb: **{ratings[i]}**")



    
    




