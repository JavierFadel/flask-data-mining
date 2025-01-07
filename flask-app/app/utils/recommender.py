import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load data
# data = pd.read_csv("../../../../dataset/data.csv")
data = pd.read_csv("dataset/data.csv")

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='66fcca3ed4a240c39f7ac585c43943aa',
                                                           client_secret='bc63f77a3eec47439e90c89378b56432'))

number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
               'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

# Define your clustering and t-SNE functions here (same as before)...
# Skipping for brevity since you've provided it earlier


def find_song(name, year):
    # Function to fetch song data from Spotify API
    song_data = defaultdict()
    results = sp.search(q='track: {} year: {}'.format(name, year), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)


def recommend_songs(song_list, spotify_data, n_songs=10):
    # Function to recommend songs based on the mean vector of given songs
    def get_mean_vector(song_list, spotify_data):
        song_vectors = []

        for song in song_list:
            song_data = get_song_data(song, spotify_data)
            if song_data is None:
                print(f"Warning: {song['name']} does not exist in Spotify or database")
                continue
            song_vector = song_data[number_cols].values
            song_vectors.append(song_vector)

        song_matrix = np.array(list(song_vectors))
        return np.mean(song_matrix, axis=0)

    def flatten_dict_list(dict_list):
        flattened_dict = defaultdict()
        for key in dict_list[0].keys():
            flattened_dict[key] = []

        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)

        return flattened_dict

    def get_song_data(song, spotify_data):
        try:
            song_data = None

            filtered_data = spotify_data[
                (spotify_data['name'] == song['name']) & (spotify_data['year'] == song['year'])
            ]

            if not filtered_data.empty:
                song_data = filtered_data.iloc[0]
                print(song_data)
            else:
                print(f"No match found for song: {song['name']} ({song['year']})")

            return song_data

        except IndexError:
            return find_song(song['name'], song['year'])

    song_dict = flatten_dict_list(song_list)

    song_center = get_mean_vector(song_list, spotify_data)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])

    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[['name', 'year', 'artists']].to_dict(orient='records')