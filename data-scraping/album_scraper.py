from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import itertools

years = [year for year in range(2002, 2023, 1)]
print(years)

album_list = []
# for year in years:
#     response = requests.get(f'https://www.billboard.com/charts/year-end/{year}/top-billboard-200-albums/')
#     soup = BeautifulSoup(response.text, "html.parser")
#     chart_results = soup.find(class_='chart-results-list')

for year in years:
    time.sleep(1.5)
    response = requests.get(f'https://www.billboard.com/charts/year-end/{year}/top-billboard-200-albums/')
    soup = BeautifulSoup(response.text, "html.parser")
    chart_results = soup.find(class_='chart-results-list')
    raw_titles = chart_results.find_all(class_='c-title')
    ranks_and_artists = chart_results.find_all(class_='c-label')

    albums = [raw_titles[i].text.strip() for i in range(len(raw_titles))]
    ranks = [int(ranks_and_artists[i].text.strip()) for i in range(0, len(ranks_and_artists), 2)]
    artists = [ranks_and_artists[i].text.strip() for i in range(1, len(ranks_and_artists), 2)]

    for (rank, artist, album) in zip(ranks, artists, albums):
        album_list.append({
            'rank': rank,
            'artist': artist,
            'album': album,
            'year': year
        })

df = pd.DataFrame(album_list)
df.to_csv('../data/albums/albums_df.csv', index=False)