import numpy as np
import pandas as pd
import pickle
import streamlit as st
import requests
from fuzzywuzzy import fuzz, process  # Make sure you have the fuzzywuzzy library installed
import base64
# Function to fetch poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)  # Replace with your API key
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path', None)  # Handle missing poster_path gracefully
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None

# Function to recommend movies
def recommend(movie):
    # Search for movie titles with typo tolerance
    matches = process.extract(movie, movies['title'], scorer=fuzz.token_set_ratio)
    relevant_matches = [match for match in matches if match[1] >= 90]

    if relevant_matches:
        # Get the closest matching title
        closest_match = relevant_matches[0][0]
        index = movies[movies['title'] == closest_match].index[0]

        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:6]:
            # Fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    else:
        return [], []

# Load movies and similarity data
movies = pickle.load(open('movie2_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Streamlit app
st.set_page_config(
    page_title="Get Good Movies",
    page_icon="🎬",
    layout="wide"
)



# Streamlit app
st.markdown("<h1 style='font-size: 60px; color: #fffebe; text-align: center;'>Feel Good Movies</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 24px; color: black; text-align: left; margin-top: 80px; margin-bottom: -40px;'>Movies that match your taste:</h3>", unsafe_allow_html=True)

search_input = st.text_input("", value='', key='search_input')

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("ash.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 100%;
background-position: top right;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: bottom-right; 
background-size: 20%;
background-repeat: repeat;
background-attachment: fixed;
background-text: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("It's summer!")
st.sidebar.markdown("<h3 style='font-size: 30px; color: #fffebe; text-align: right center; margin-top:-80px;margin-left:135px'>Hey, it's me</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 class='css-6qob1r eczjsme3' style='font-size: 30px; color: #be254a; margin-top: 55px; margin-bottom: 300px;margin-left: 90px;'>Good pick  </h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 class='css-6qob1r eczjsme3' style='font-size: 30px; color: #60bba8; margin-top: -140px; margin-bottom: 300px;margin-left: 110px;'>Have fun </h3>", unsafe_allow_html=True)



poster_length = 125  # Set width of each poster to 125

if search_input:
    recommended_movie_names, recommended_movie_posters = recommend(search_input)
    num_recommendations = len(recommended_movie_names)

    cols = st.columns(num_recommendations)

    col_spacing = 10  # Adjust this value to set the spacing between posters

    with cols[0]:
        st.image(recommended_movie_posters[0], width=poster_length)
        st.markdown("<h4 style='color: white; margin-top: 5px;'>" + recommended_movie_names[0] + "</h4>", unsafe_allow_html=True)
    with cols[1]:
        st.image(recommended_movie_posters[1], width=poster_length)
        st.markdown("<h4 style='color: white; margin-top: 5px;'>" + recommended_movie_names[1] + "</h4>", unsafe_allow_html=True)

    with cols[2]:
        st.image(recommended_movie_posters[2], width=poster_length)
        st.markdown("<h4 style='color: white; margin-top: 5px;'>" + recommended_movie_names[2] + "</h4>", unsafe_allow_html=True)
    with cols[3]:
        st.image(recommended_movie_posters[3], width=poster_length)
        st.markdown("<h4 style='color: white; margin-top: 5px;'>" + recommended_movie_names[3] + "</h4>", unsafe_allow_html=True)
    with cols[4]:
        st.image(recommended_movie_posters[4], width=poster_length)
        st.markdown("<h4 style='color: white; margin-top: 5px;'>" + recommended_movie_names[4] + "</h4>", unsafe_allow_html=True)
