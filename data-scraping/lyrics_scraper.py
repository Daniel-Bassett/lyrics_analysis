from bs4 import BeautifulSoup
import pandas as pd
import requests
import itertools
from lyricsgenius import Genius
from config import *

# load song titles and artists information
christian_songs_df = pd.read_csv('data\songs\Christian.csv')
hip_hop_df = pd.read_csv('data\songs\Hip-Hop-RB.csv')
pop_df = pd.read_csv('data\songs\Pop.csv')
rock_df = pd.read_csv('data\songs\Rock.csv')
country_df = pd.read_csv('data\songs\Country.csv')
electro_df = pd.read_csv('data\songs\Electro-Dance.csv')

genius = Genius(TOKEN, remove_section_headers=True, sleep_time=1)

dataframes = [christian_songs_df, hip_hop_df, pop_df, rock_df, country_df, electro_df]
labels = ['Christian', 'Country', 'Electro-Dance', 'Hip-Hop-RB', 'Pop', 'Rock']

for (dframe, label) in zip(dataframes, labels):
    lyrics_list = []
    for row, col in dframe.iterrows():
        print(col['title'], col['artist'], col['year'])
        try:
            song = genius.search_song(col['title'], col['artist'])
            lyrics = song.lyrics.split()
            for word in lyrics:
                lyrics_list.append({
                    'word': word,
                    'artist': col['artist'],
                    'title': col['title'],
                    'year': col['year'],
                    'genre': col['genre'],
                    'rank': col['rank']
            })
        except:
            print('-----------There was an ERROR here-----------')
            print(col['title'], col['artist'], col['year'])
            print('-----------There was an ERROR here-----------')
    df = pd.DataFrame(lyrics_list)
    df.to_csv(f'data\lyrics\{label}lyrics.csv')