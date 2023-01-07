from bs4 import BeautifulSoup
import requests
import time
import itertools

response = requests.get('https://www.billboard.com/charts/year-end/2013/hot-dance-electronic-songs/')
soup = BeautifulSoup(response.text, "html.parser")
chart_results = soup.find(class_='chart-results-list')
raw_titles = chart_results.find_all(class_='c-title')
ranks_and_artists = chart_results.find_all(class_='c-label')

titles = [raw_titles[i].text.strip() for i in range(len(raw_titles))]
ranks = [int(ranks_and_artists[i].text.strip()) for i in range(0, len(ranks_and_artists), 2)]
artists = [ranks_and_artists[i].text.strip() for i in range(1, len(ranks_and_artists), 2)]

for (rank, artist, titles) in zip(ranks, artists, titles):
    print(rank, artist, titles)