import plotly_express as px
import streamlit as st
import pandas as pd

# load the data
df = pd.read_csv('..\data\lyrics\clean_df.csv')
word_count = pd.read_csv('..\data\lyrics\word_count.csv')

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
    st.header('Compare Words by Genre')
    st.write('This shows the frequency of words by genre.')
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


def main():
    st.title('Top Five Words by Genre')
        # top 5 words for one genre
    st.header('Introduction')
    st.write(
        'This shows the top words by percentage of songs that contains the word in their lyrics.'
        'The first two charts show the word "love" appearing in 62.2\% of all Christian songs and 57.5\% of all Electro-Dance songs.'
    )

    # this generates bar charts
    genres = word_count['genre'].unique()
    genres_choice = st.multiselect('Choose genres to compare', genres, default=['Christian', 'Electro-Dance'])
    bar_charts(genres_choice, word_count)
    grouped_histogram(word_count)


    # with st.expander('Line Chart of Word Popularity', expanded=True):
    #     words = new_df['word'].unique()
    #     words_choice = st.multiselect('Choose words to compare', words, default=['beer', 'whiskey'])
    #     if words_choice:
    #         temp_df_list = []
    #         for word in words_choice:
    #             temp_df = new_df.groupby('year')['word'].value_counts().unstack()[word].to_frame()
    #             temp_df['word'] = word
    #             temp_df.rename(columns={word: 'count'}, inplace=True)
    #             temp_df.reset_index(inplace=True)
    #             temp_df_list.append(temp_df)
    #         plotting_df = pd.concat(temp_df_list)
    #         plotting_df.fillna(0, inplace=True)
    #         x_plot = plotting_df['year']
    #         y_plot = plotting_df['count']
    #         line_plots = px.line(data_frame=plotting_df, x='year', y='count', title='The Number of Top Country Songs a Word Appears in by Year', color='word', labels={'count': 'Song Count', 'year': 'Year'})
    #         line_plots.update_layout(title_x=0.5)
    #         st.plotly_chart(line_plots, use_container_width=True)

# horizontal barchart of one word percentage
# word = 'beer'
# genre = 'Country'
# word_count = word_count_df[(word_count_df['genre'] == genre) & (word_count_df['word'] == word)]['count']
# country_song_count = len(df[df['genre'] == genre]['title'].unique())
# temp_df = word_count_df[(word_count_df['genre'] == genre) & (word_count_df['word'] == word)]
# barh_plot = px.bar(y=percentage, orientation='h')


    
if __name__ == '__main__':
    main()

