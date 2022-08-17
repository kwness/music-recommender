
# Streamlit app hosting the recommender system as built. Updating the text box with various lists of songs will return
# 10 recommendations of similar ones at once. Note: taking the mean of very different songs may yield fruitless recommendations.

import pandas as pd
import numpy as np
import spotipy
import sys
sys.path.insert(0, '../../../')
from api_keys import client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

import streamlit as st
import pandas as pd

tracks = pd.read_csv('../data/cleaned/track_data.csv')
meta_scaled = pd.read_csv('../data/cleaned/scaled_with_metadata.csv')

tracks = pd.read_csv('../data/cleaned/track_data.csv')
meta_scaled = pd.read_csv('../data/cleaned/scaled_with_metadata.csv')

#Below, a lot of this code is taken directly from the recommender.ipynb file. Easiest way of getting this running fluidly.

ss = StandardScaler()
ss.fit(tracks.select_dtypes(include = 'number').drop(columns = 'year'))

# Using spotipy's SpotifyOAuth class so that we can use spotify's API w/ proper authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

def get_scaled_feats(song):
    '''
    Helper function to recommend(). Takes a song as input in the form (tile, release year) and returns a dataframe
    containing that song's scaled audio features.
    
    If song is available in the downloaded scaled tracks data, will fetch from there. Otherwise,
    uses spotipy to grab the song's audio features from Spotify, then scales them.
    '''
    name, year = song
    track_df = meta_scaled[(meta_scaled['name'] == name) & (meta_scaled['year'] == year)]
    track_df = track_df.copy(deep = True) # Was giving a warning otherwise (changing value of a slice)
    if len(track_df) != 0:
        track_df.reset_index(drop = True)
        return pd.DataFrame([track_df.iloc[0]]).drop(columns = ['name','artists', 'year', 'genre'])
    else:
        song_data = {}
        fetch = sp.search(q = f'track: {name} year: {year}', limit = 1)
        if fetch['tracks']['items'] != []:
            features = sp.audio_features(fetch['tracks']['items'][0]['id'])[0] # Grabbing 1st / most relevant search result
            del features['track_href'], features['analysis_url'], features['uri'], features['type']
            song_data['explicit'] = int(fetch['tracks']['items'][0]['explicit'])
            song_data['popularity'] = fetch['tracks']['items'][0]['popularity']
            for key, value in features.items():
                song_data[key] = value
            song_data.pop('id')
            df_cols = song_data.keys()
            return pd.DataFrame(ss.transform(pd.DataFrame([song_data])), columns = df_cols)
        else:
            return None 

def recommend(songlist, n = 5):
    '''
    Taking in a list of songs, each of the format (title, release year), returns n songs as
    recommendations for the user to explore.
    
    Note: These recommendations are only sourced from the downloaded data, not from all of spotify's
    available songs.
    '''
    vectors = pd.DataFrame()
    name_list = []
    for song in songlist:
        name, year = song
        name_list.append(name)
        vector = get_scaled_feats(song)
        if vector is None:
            print(f'{name} cannot be found on Spotify! Sorry.')
            continue
        else:
            vectors = pd.concat([vectors, vector])
    # Creating centroid vector (already scaled)
    centroid =  pd.DataFrame(vectors.mean(numeric_only = True)).T
    # Calculating distances from centroid for all tracks -- looking for closest ones
    distances = cdist(centroid.iloc[:,:], meta_scaled.select_dtypes(include = 'number').drop(columns = 'year').iloc[:,:], 'cosine') 
    distances = pd.DataFrame({'distance': distances[0]}).sort_values('distance', ascending = True)
    index = list(distances.index[:n])
    recs = tracks.iloc[index]
    recs = recs[~recs['name'].isin(name_list)]
    recs.reset_index(drop = True, inplace = True)
    return recs[['name', 'artists', 'year', 'genre']]

def stripper(txt):
    lst = []
    for x in txt.split(';'):
        lst.append((x.split(',')[0].strip(), int(x.split(',')[1])))
    return lst

st.title('Spotify Song Recommender')

st.subheader('Provide a list of songs (minimum 1) to be recommended similar tunes.')

txt = st.text_input('Format each song as "title, release year", seperating entries by a semicolon. Ex: Firework, 2012; Piano Man, 1973').strip()

X = stripper(txt)

st.subheader("Based on these songs' audio features, you may like:")

st.write(recommend(X, 10))
