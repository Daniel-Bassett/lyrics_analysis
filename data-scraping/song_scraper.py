from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import itertools

years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
genre = 'pop'

lyrics_list = []

for year in years:
    print(year)
    time.sleep(3)
    response = requests.get(f'https://www.billboard.com/charts/year-end/{year}/pop-songs/')
    soup = BeautifulSoup(response.text, "html.parser")
    chart_results = soup.find(class_='chart-results-list')
    raw_titles = chart_results.find_all(class_='c-title')
    ranks_and_artists = chart_results.find_all(class_='c-label')

    titles = [raw_titles[i].text.strip() for i in range(len(raw_titles))]
    ranks = [int(ranks_and_artists[i].text.strip()) for i in range(0, len(ranks_and_artists), 2)]
    artists = [ranks_and_artists[i].text.strip() for i in range(1, len(ranks_and_artists), 2)]

    for (rank, artist, title) in zip(ranks, artists, titles):
        
        lyrics_list.append({
            'title': title,
            'artist': artist,
            'rank': rank,
            'genre': genre
        })
    
df = pd.DataFrame(lyrics_list)
df.to_csv('data/pop.csv', index=False)