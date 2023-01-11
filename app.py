import plotly_express as px
import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder
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
album_df = load_model('data/albums/albums_df.csv')

# manipulate data
artist_rank_year = album_df[['rank', 'artist', 'year']].groupby(['artist', 'year'])['rank'].min().to_frame().reset_index()


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
                    bar_plots.update_layout(title_x=0.5, showlegend=True, height=600)
                    st.plotly_chart(bar_plots, use_container_width=True)
        else:
            with col2: 
                with st.expander(genre, expanded=True):
                    temp_df = top_5[top_5['genre'] == genre]
                    bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
                    bar_plots.update_layout(title_x=0.5, showlegend=True, height=600)
                    st.plotly_chart(bar_plots, use_container_width=True)


def grouped_histogram(df):
    col1, col2  = st.columns([1, 3])
    word_count = df
    word_options = word_count[word_count['count'] > 3]['word'].unique() # I reduced the number of words available in order to improve performance of app
    with col1:
        words_choice = st.multiselect(options=word_options, label='Choose Words to Compare', default=['girl', 'boy'])
    temp_df = word_count[word_count['word'].isin(words_choice)]
    col3, col4 = st.columns([5, 1])
    with col3:
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
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)


def line_chart_lyrics(df):
    counts_by_year = df
    # multiselect from user
    col1, col2 = st.columns(2)
    with col1:
        genres = counts_by_year['genre'].unique()
        genre_choice = st.multiselect(options=genres, default=['Country'],label='Choose a Genre')
   
        words = counts_by_year[counts_by_year['count'] > 2]['word'].unique()
        word_choice = st.multiselect(options=words, default=['whiskey', 'beer'], label='Choose Words to Compare')
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


def line_chart_artists(df):
    # import data and organize
    artist_rank_year = df
    artists = artist_rank_year[artist_rank_year['artist'].map(artist_rank_year['artist'].value_counts() > 1)]['artist'].unique() # filtered out artists that charted for only one year
    # get user input
    col1, col2 = st.columns([1, 4])
    with col1: # use columns for padding
        artist_choice = st.multiselect(options=artists, label='Choose artists', default=['Taylor Swift', 'Drake'])
    artist_mask = artist_rank_year['artist'].isin(artist_choice)
    dataframe = artist_rank_year[artist_mask]
    # plot the data
    col2, col3 = st.columns([5, 1])
    with col2:
        fig = px.line(data_frame=dataframe, x='year', y='rank', color='artist')
        fig.update_layout(xaxis = dict(tick0=2001, dtick=3), height=600)
        fig.update_yaxes(autorange='reversed', mirror=False)
        st.plotly_chart(fig, use_container_width=True)


def artist_average_table(df):

    album_df = df
    # create a table
    no_duplicate_albums = album_df[['artist', 'album']].drop_duplicates()

    # get user input on min and max number of albums to filter
    min_albums = st.number_input('minimum albums', min_value=1)
    max_albums = st.number_input('maximum albums', min_value=1)

    # calculates the number of unique albums each artist has and filters out the artist based on number of albums
    min_max_albums_mask = no_duplicate_albums['artist'].map(no_duplicate_albums['artist'].value_counts().between(min_albums, max_albums))

    # creates an array of unique names that meet meet the min_max albums criteria
    artists = no_duplicate_albums[min_max_albums_mask]['artist'].unique()

    # find the mean rank of all artists' albums
    mean_of_artist_rank = album_df.groupby(['artist', 'album'])['rank'].min().to_frame().reset_index().groupby(['artist'])['rank'].mean().to_frame().reset_index()
    
    # only return the artists that meet the min_max criteria
    mean_of_artist_filtered = mean_of_artist_rank[mean_of_artist_rank['artist'].isin(artists)].sort_values(by='rank')

    # create dataframe of counts of unique albums for each artist and filter them out based on min_max criteria
    album_counts = no_duplicate_albums[min_max_albums_mask]['artist'].value_counts().to_frame().reset_index().rename({'artist': 'album count', 'index': 'artist'}, axis=1)

    # merge mean of artists filtered with album counts
    table = pd.merge(mean_of_artist_filtered, album_counts).rename({'rank': 'average rank of albums (end of year)', 'count': 'total unique albums'}, axis=1)


def aggrid_table(df):
    album_df = df
    # create a table
    no_duplicate_albums = album_df[['artist', 'album']].drop_duplicates()

    # create columns for user input 
    col1, col2, col3 = st.columns([1, 1, 5])
    # get user input on min and max number of albums to filter
    with col1:
        min_albums = st.number_input('Artist has at least this many albums', min_value=1, value=5)
    with col2:
        max_albums = st.number_input('Artist has at most this many albums', min_value=1, value=20)
        

    # calculates the number of unique albums each artist has and filters out the artist based on number of albums
    min_max_albums_mask = no_duplicate_albums['artist'].map(no_duplicate_albums['artist'].value_counts().between(min_albums, max_albums))

    # creates an array of unique names that meet meet the min_max albums criteria
    artists = no_duplicate_albums[min_max_albums_mask]['artist'].unique()

    # find the mean rank of all artists' albums
    mean_of_artist_rank = album_df.groupby(['artist', 'album'])['rank'].min().to_frame().reset_index().groupby(['artist'])['rank'].mean().to_frame().reset_index()
    
    # only return the artists that meet the min_max criteria
    mean_of_artist_filtered = mean_of_artist_rank[mean_of_artist_rank['artist'].isin(artists)].sort_values(by='rank')

    # create dataframe of counts of unique albums for each artist and filter them out based on min_max criteria
    album_counts = no_duplicate_albums[min_max_albums_mask]['artist'].value_counts().to_frame().reset_index().rename({'artist': 'album count', 'index': 'artist'}, axis=1)

    # merge mean of artists filtered with album counts
    final_df = pd.merge(mean_of_artist_filtered, album_counts).rename({'rank': 'average rank of albums (end of year)', 'count': 'total unique albums'}, axis=1)

    # create columns
    col1, col2 = st.columns([2, 3])

    # create the Ag grid
    with col1:
        gd = GridOptionsBuilder.from_dataframe(final_df.head(100))
        gd.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gd.configure_selection('single')
        grid_options = gd.build()
        st.markdown('#### Average Rank of Artist Albums')
        table = AgGrid(final_df.head(1000), gridOptions=grid_options)
        if table.selected_rows:
            name = table.selected_rows[0]['artist']
        st.caption('Click on a name to view discography')
        


    # use variable "name" to make discography 
    with col2:
        if table.selected_rows:
            min_album_rank = album_df.groupby(['artist', 'album'])['rank'].min().to_frame().reset_index()
            discography = min_album_rank[min_album_rank['artist'] == name].drop('artist', axis=1).reset_index(drop=True)
            st.markdown(f'#### {name}\'s Top 200 Discography')
            st.dataframe(discography, use_container_width=True)

    


def main():
    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',
            options=['Introduction', 'Top Five Words by Genre', 'Word Popularity by Year', 'Lyrics by Genre', 'Artist Rankings', 'Average Rank of Albums']
        )
    if selected == 'Introduction':
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title('Introduction')
            st.write(
                'Have you ever been listening to country music and noticed a trend? They all seem to sing about the same things... trucks, lakes, beer, and whiskey. '
                'Or maybe you\'re a hip-hop enthusiast and noticed that a lot of lyrics are really NSFW. '
                'Are you curious about how your favorite singers have been ranking on the charts over the years? '
                'Who is better? Taylor Swift or Drake? Let\'s find out using data! '
                'This fun little project proved challenging, but it was a blast. I hope you find this fun as well!'
                )
            st.markdown('')
            st.write(
                'First, I needed some data! Using beautifulsoup I scraped all the songs, artists, and albums from Billboard across six different genres. '
                'Once scraped, I output the data in csv format using pandas. This allowed me to iterate over every artist and song title '
                'so that I could then scrape the corresponding lyrics data off of genius using an API. Once I had all the lyrics in csv format, I used pandas '
                'to clean and rearrange the data into a format fit for use.'
            )
            # st.image('images/lyrics-scraper-code.png', width=500, caption='The code for scraping lyrics')
            st.markdown('')
            st.write(
                'Using pandas, I merged all the dataframes from each genre into one large dataframe. I then stripped chars that were unnecessary(&!?,) '
                'and often found themselves tacked on to words. I applied a stop word filter to delete all of stop words. I then dropped all the duplicates so that a word is counted '
                'only one time for each song in which they appear. Using multi-indexing, filtering, and other techniques, I created a few csv files of dataframes that I found useful for my project. '
            )
            # st.image('images/clean-data.png', caption='How I cleaned rearranged the data')
            st.markdown('')
            st.write(
                'Finally I was able to use cleaned and organized data. Streamlit and plotly were great tools for visualization and making an interactive application. '
                'very quickly.'
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
        st.header('Lyrics by Genre')
        st.write('This shows the frequency of words by genre.')
        grouped_histogram(word_count)
    if selected == 'Word Popularity by Year':
        st.header('Word Popularity by Year')
        st.write('Using a line graph, this shows the percentage of songs a word appears in through the years.')
        line_chart_lyrics(counts_by_year)
    if selected == 'Artist Rankings':
        st.header('Artist Rankings by Year')
        st.write('Take a look at your favorite artist\'s performance over the years!' )
        line_chart_artists(artist_rank_year)
    if selected == 'Average Rank of Albums':
        # aggrid
        st.header('Average Rank of Albums')
        st.write(
            'Every year, Billboard releases the Top 200 album rankings based on sales as well as audio on-demand streaming activity and digital sales of tracks from albums. '
            'This calculates the average rank for an all of an artist\'s albums that have made it into the top 200. '
            'You can filter this list based on the number of Top 200 albums the artist has made. For example, if you set min equal to \'5\' and max to \'20\', '
            'it will return all the artists who have made anywhere from 5 to 20 albums that made it on the Top 200 charts. '
            'Click on an artist\'s name on the table to get a snapshot of their discography'
        )
        aggrid_table(album_df)
        # st.dataframe(artist_average_table(album_df))
        



if __name__ == '__main__':
    main()

