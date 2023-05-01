# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 23:52:05 2023
pip inst
@author: knksh
"""

import pandas as pd 
import numpy as np
import streamlit as st
import pickle 
import requests

st.title('Netflix Content Recommendor')
movie_list = pickle.load(open('c:/Users/knksh/Desktop/modeldeployment/movies_for_rec.pkl','rb'))
indices = pd.Series(movie_list.index)
options = st.selectbox(
    'What would you like to watch?', (indices))

cosine_sim = pickle.load(open('c:/Users/knksh/Desktop/modeldeployment/cosine_sim.pkl','rb')) 

# fetch items Tv- shows
# https://api.themoviedb.org/3/search/tv?api_key=ff24c67ac70071d5695f091eb82e1264&language=en-US&page=1&query=13%20Reasons%20Why%3A%20Beyond%20the%20Reasons&include_adult=false
# fetch items movies
# https://api.themoviedb.org/3/search/movie?api_key=ff24c67ac70071d5695f091eb82e1264&language=en-US&query=Batman&page=1&include_adult=false

def recommend(Title, cosine_sim = cosine_sim):
    
    recommended_movies = []
    idx = indices[indices == Title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:6].index)
    for i in top_10_indexes:
        recommended_movies.append(list(movie_list.index)[i])
        
    return recommended_movies


if st.button('Recommend'):
    recommendations = recommend(options)
    for i in recommendations:
        st.write(i)

def fetch_poster(i):
    response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=ff24c67ac70071d5695f091eb82e1264&language=en-US&query={}&page=1&include_adult=false').format(i)
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
