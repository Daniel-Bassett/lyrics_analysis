import plotly_express as px
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np

# set the page layout
st.set_page_config(layout='wide')

# load the data
@st.experimental_memo
def load_model(csv_path):
    df = pd.read_csv(csv_path)
    return df

df = load_model('data/lyrics/clean_df.csv')
word_count = load_model('data/lyrics/word_count.csv')
counts_by_year = load_model('data/lyrics/word_count_year.csv')


def bar_charts(genres_choice, df):
    top_5 = df
    col1, col2 = st.columns(2)
    top_5 = word_count.groupby('genre').head().sort_values(by=['genre', 'percentage'], ascending=False)
    for genre in genres_choice:
        if genres_choice.index(genre) % 2 == 0:
            with col1:
                with st.expander(genre, expanded=True):
                    temp_df = top_5[top_5['genre'] == genre]
                    bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
                    bar_plots.update_layout(title_x=0.5, showlegend=True)
                    st.plotly_chart(bar_plots, use_container_width=True)
        else:
            with col2: 
                with st.expander(genre, expanded=True):
                    temp_df = top_5[top_5['genre'] == genre]
                    bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
                    bar_plots.update_layout(title_x=0.5, showlegend=True)
                    st.plotly_chart(bar_plots, use_container_width=True)


def grouped_histogram(df):
    word_count = df
    word_options = word_count[word_count['count'] > 3]['word'].unique() # I reduced the number of words available in order to improve performance of app
    words_choice = st.multiselect(options=word_options, label='Choose Words to Compare', default=['girl', 'boy'])
    temp_df = word_count[word_count['word'].isin(words_choice)]
    fig = px.bar(
        data_frame=temp_df, 
        x='word', 
        y='percentage', 
        color='genre', 
        barmode='group',
        text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)),
        orientation='v',
        )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig)


def line_chart_year(df):
    counts_by_year = df
    # multiselect from user
    col1, col2 = st.columns(2)
    with col1:
        genres = counts_by_year['genre'].unique()
        genre_choice = st.multiselect(options=genres, default=['Country', 'Hip-Hop-RB'],label='Choose a Genre')
   
        words = counts_by_year[counts_by_year['count'] > 2]['word'].unique()
        word_choice = st.multiselect(options=words, default=['girl', 'boy'], label='Choose Words to Compare')
    # creates mask from the mutliselect genres
    genre_mask = counts_by_year['genre'].isin(genre_choice)
    # plot line
    col3, col4 = st.columns(2)
    for word in word_choice:
        if word_choice.index(word) % 2 == 0:
            with col3:
                with st.expander(label=str(word).upper(), expanded=True):
                    word_mask = counts_by_year['word'] == word
                    fig = px.line(data_frame=counts_by_year[genre_mask & word_mask], x='year', y='percentage year', color='genre', title=f'Comparisons for the word {str(word).upper()}')
                    fig.update_layout(
                    yaxis_title='Percentage of Songs',
                    xaxis = dict(tick0=2012, dtick=1)
                    )
                    st.plotly_chart(fig)
        else:
            with col4:
                with st.expander(label=str(word).upper(), expanded=True):
                    word_mask = counts_by_year['word'] == word
                    fig = px.line(data_frame=counts_by_year[genre_mask & word_mask], x='year', y='percentage year', color='genre', title=f'Comparisons for the word {str(word).upper()}')
                    fig.update_layout(
                    yaxis_title='Percentage of Songs',
                    xaxis = dict(tick0=2012, dtick=1)
                    )
                    st.plotly_chart(fig)
    


def main():
    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',
            options=['Introduction', 'Top Five Words by Genre', 'Word Popularity by Year', 'Lyrics by Genre']
        )
    if selected == 'Introduction':
        st.title('Introduction')
        st.write(
            'Have you ever been listening to country music and noticed a trend? They all seem to sing about the same things... trucks, lakes, beer, and whiskey. '
            'Or maybe you\'re a hip-hop enthusiast and noticed that a lot of lyrics are really NSFW. '
            'In order to explore this, I first "scraped" together all the top songs and artists from [Billboard\'s](#https://www.billboard.com/) Top 100 Songs for the years 2013 through 2022 using beautifulsoup. '
            'I then scraped the lyrics off [genius](#https://genius.com/) using the lyrics genius API and put them into csv format. Using pandas, I cleaned the data and manipulated it into dataframes that I found useful. '
            'Finally, I made an app to visualize this data in an interactive and fun way that I hope you will enjoy!'
            )
        st.markdown('### Let\'s get some data!')
        st.write(
            'First, I needed some data! Using beautifulsoup I scraped all the song and artists from Billboard across six different genres. '
            'Once scraped, I output the data in csv format using pandas. This allowed me to iterate over every artist and song title '
            'so that I could then scrape the corresponding data off of genius using an API. Once I had all the lyrics in csv format. I used pandas '
            'to clean and rearrange the data into a format fit for use.'
        )
        st.image('images/lyrics-scraper-code.png', width=500, caption='The code for scraping lyrics')
        st.markdown('### Cleaning the Data')
        st.write(
            'Using pandas, I merged all the dataframes from each genre into one large dataframe. I then stripped chars that were unnecessary(&!?,) '
            'and often found themselves tacked on to words. I applied a stop word filter to delete all of stop words. I then dropped all the duplicates so that a word is counted '
            'only one time for each song in which they appear. Using multi-indexing, filtering, and other techniques, I created a few csv files of dataframes that I found useful for my project:'
        )
        st.image('images/clean-data.png', caption='How I cleaned rearranged the data')
        st.markdown('### Visualization of Data')
        st.write(
            'Using the cleaned and organized data, streamlit and plotly were great tools for visualization and making an interactive application. '
            'Just import the data and with a few lines of code you can have some cool looking graphs that are interactive.'
        )
    if selected == 'Top Five Words by Genre':
        st.title('Top Five Words by Genre')
        st.write(
            'This shows the top words by percentage of songs that contain the word in their lyrics respective of genre. '
            'The first two charts show the word "love" appearing in 62.2\% of all Christian songs and 57.5\% of all Electro-Dance songs. '
            'Feel free to add/subtract genres to compare!'
            )
        genres = word_count['genre'].unique()
        genres_choice = st.multiselect('Choose genres to compare', genres, default=['Christian', 'Electro-Dance'])
        bar_charts(genres_choice, word_count)
    if selected == 'Lyrics by Genre':
        st.header('Compare Words by Genre')
        st.write('This shows the frequency of words by genre.')
        grouped_histogram(word_count)
    if selected == 'Word Popularity by Year':
        st.header('Word Popularity by Year')
        st.write('Using a line graph, this shows the percentage of songs a word appears in through the years by genre.')
        line_chart_year(counts_by_year)
    
if __name__ == '__main__':
    main()

