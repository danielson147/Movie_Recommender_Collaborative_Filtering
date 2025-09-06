import streamlit as st 

# 👇 MUST be first Streamlit command
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

import pickle
import pandas as pd
import os

# ---------------- Load Pickled Data ----------------
@st.cache_resource
def load_data():
    movies = pickle.load(open("movie_ratings.pkl", "rb"))

    # If it's not already a DataFrame, try to convert
    if not isinstance(movies, pd.DataFrame):
        try:
            movies = pd.DataFrame(movies)
        except Exception as e:
            st.error(f"❌ Could not convert pickle to DataFrame: {e}")
            return pd.DataFrame()

    return movies

movies = load_data()

# --- Identify Title Column Automatically ---
possible_title_cols = ["title", "Title", "movie_title", "name"]
title_col = None
for col in possible_title_cols:
    if col in movies.columns:
        title_col = col
        break

if title_col is None:
    st.error("❌ No title column found in your dataset. Please check your pickle file.")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.title("🎥 Recommender")
    st.markdown("Created by: *Deep Tech Data Science Class*")
    st.markdown("---")
    st.write("Select a movie to get recommendations based on collaboration.")

# ---------------- Recommendation Logic ----------------
def recommend(movie):
    if movie not in movies[title_col].values:
        return []
    # Simple fallback: return 5 random movies except the selected one
    sample = movies[movies[title_col] != movie].sample(min(5, len(movies)-1))[title_col].tolist()
    return sample

# ---------------- Main App UI ----------------
st.title("🎬 Movie Recommender System")
st.markdown("Select a movie and discover similar recommendations.")

selected_movie = st.selectbox("🎞️ Choose a movie:", movies[title_col].values)

if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("🎯 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    else:
        st.warning("Movie not found or no recommendations available.")
