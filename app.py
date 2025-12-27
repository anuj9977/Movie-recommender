import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6c8e315be70cf151271f6dd5c15b8780&language=en-US'.format(movie_id))
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"  # Default placeholder image

def recommend(movie):
  movie_index=movies[movies['title']==movie].index[0]
  dis=similarity[movie_index]
  movie_list=sorted(list(enumerate(dis)),reverse=True,key=lambda x:x[1])[1:6]

  recommended_movies=[]
  recommended_posters=[]
  for i in movie_list:
    recommended_movies.append(movies.iloc[i[0]].title)
    recommended_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
  return recommended_movies, recommended_posters


movies_list = pickle.load(open('movie_dict', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies=pd.DataFrame(movies_list)



st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Select your favorite Movie:',
    movies['title'].values
)
if st.button('Recommend'):
    names,poster=recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
    