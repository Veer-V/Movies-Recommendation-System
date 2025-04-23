import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load the data
movies_dict = pickle.load(open('C:/Users/Osama/OneDrive/Desktop/MovieRecommendationSysytems/movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('C:/Users/Osama/OneDrive/Desktop/MovieRecommendationSysytems/similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Streamlit UI
st.title("Movies Recommendation System")

selected_movie_name = st.selectbox(
    'What would you like to watch?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.subheader("Recommended Movies:")
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx])
            st.caption(names[idx])
