from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import itertools
from lyricsgenius import Genius
from config import *

genius = Genius(TOKEN, remove_section_headers=True)



christian_songs_df = pd.read_csv('data\christian.csv')
print(christian_songs_df)

lyrics_list = []



for row, col in christian_songs_df.iterrows():
    song = genius.search_song(col['title'], col['artist'])
    lyrics = song.lyrics.split()
    for word in lyrics:
        lyrics_list.append({
            'word': word,
            'artist': col['artist'],
            'title': col['title'],

        })
