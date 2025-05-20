import pickle
import streamlit as st
import requests

# Function to fetch movie poster using TMDB movie ID
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=48dbfa77008c976c9a4e274163e7592d&language=en-US"
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=48dbfa77008c976c9a4e274163e7592d&language=en-US")
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        print("Poster fetch error:", e)
        return "https://via.placeholder.com/300x450?text=Error"

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

#Streamlit UI
st.header('🎬 Movie Recommender System Using Machine Learning')

# Load saved movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))  # DataFrame with 'title' and 'movie_id' columns
similarity = pickle.load(open('similarity.pkl', 'rb'))  # 2D list or numpy array

#  User input dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

