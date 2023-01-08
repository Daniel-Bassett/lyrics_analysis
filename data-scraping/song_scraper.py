from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import itertools

labels = ['Christian', 'Country', 'Electro-Dance', 'Hip-Hop-RB', 'Pop', 'Rock']
urls = ['hot-christian-songs','hot-country-songs', 'hot-dance-electronic-songs', 'hot-r-and-and-b-hip-hop-songs','pop-songs', 'hot-rock-songs']
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]


for (url, label) in zip(urls, labels):
    song_list = []
    for year in years:
        print(year, label)
        time.sleep(2)
        response = requests.get(f'https://www.billboard.com/charts/year-end/{year}/{url}/')
        soup = BeautifulSoup(response.text, "html.parser")
        chart_results = soup.find(class_='chart-results-list')
        raw_titles = chart_results.find_all(class_='c-title')
        ranks_and_artists = chart_results.find_all(class_='c-label')

        titles = [raw_titles[i].text.strip() for i in range(len(raw_titles))]
        ranks = [int(ranks_and_artists[i].text.strip()) for i in range(0, len(ranks_and_artists), 2)]
        artists = [ranks_and_artists[i].text.strip() for i in range(1, len(ranks_and_artists), 2)]

        for (rank, artist, title) in zip(ranks, artists, titles):
            
            song_list.append({
                'title': title,
                'artist': artist,
                'rank': rank,
                'genre': label,
                'year': year
            })
    
    df = pd.DataFrame(song_list)
    df.to_csv(f'data/{label}.csv', index=False)