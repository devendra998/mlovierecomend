import streamlit as st
import pickle
import pandas as pd


movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie, num_recommendations=5):
    movie_indx = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_indx]
    recommended_movies = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recommendations+1]

    recommended_movie_titles = []
    for i in recommended_movies:
        recommended_movie_titles.append(movies.iloc[i[0]]['title'])
    return recommended_movie_titles


st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation System 🍿")
st.subheader("Find your next favorite movie! 😍")


st.markdown("""
    ## Welcome to the Movie Recommendation System!  
    Get personalized movie recommendations based on your favorites.  
    Simply select a movie and we will suggest similar ones to keep you entertained.  
    Happy watching! 🎥
""")


selected_movie_name = st.selectbox(
    "Pick a movie to get recommendations:",
    options=movies['title'].values,
    key="movie_selectbox"
)


num_recommendations = st.slider(
    "How many recommendations would you like?",
    min_value=1, max_value=10, value=5, step=1,
    key="num_recommendations_slider"
)

def display_movie_with_poster(movie_name):
    try:
        movie_data = movies[movies['title'] == movie_name].iloc[0]
        poster_url = movie_data.get('poster_url', '')
        if poster_url:
            st.image(poster_url, caption=movie_name, width=150)
        else:
            st.warning("Poster not available.")
    except IndexError:
        st.error("Movie not found in the dataset!")

display_movie_with_poster(selected_movie_name)

if st.button("Recommend Movies", key="recommend_button"):
    with st.spinner('Generating movie recommendations...'):
        recommendations = recommend(selected_movie_name, num_recommendations)

    st.subheader("Recommended Movies 🍿")
    
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for idx, movie in enumerate(recommendations):
        with cols[idx % 3]:  
            st.write(f"**{movie}**")
            display_movie_with_poster(movie)

    st.success("Done!")

st.markdown("""
    <style>
        footer {visibility: hidden;} 
    </style>
    <footer>
        <p style='text-align: center;'>Made with ❤️ by Devendra </p>
    </footer>
""", unsafe_allow_html=True)

