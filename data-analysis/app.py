import plotly_express as px
import streamlit as st
import pandas as pd

# load the data
df = pd.read_csv('..\data\lyrics\clean_df.csv')
word_count = pd.read_csv('..\data\lyrics\word_count.csv')

def main():
    st.title('Lyrics Analysis')
        # top 5 words for one genre
    st.header('Top Five Words by Genre')
    st.write(
        'This shows the top words by percentage of songs that contains the word in their lyrics.'
        'The first two charts show the word "love" appearing in 62.2\% of all Christian songs and 57.5\% of all Electro-Dance songs.'
    )

    col1, col2 = st.columns(2)
    top_5 = word_count.groupby('genre').head().sort_values(by=['genre', 'percentage'], ascending=False)
    with col1: 
        genre = 'Christian'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre, expanded=True):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True)    
        genre = 'Rock'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True)   
        genre = 'Pop'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True) 

    with col2:
        genre = 'Electro-Dance'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre, expanded=True):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True) 
        genre = 'Country'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True) 
        genre = 'Hip-Hop-RB'
        temp_df = top_5[top_5['genre'] == genre]
        with st.expander(label=genre):
            bar_plots = px.bar(data_frame=temp_df, x='word', y='percentage', title=genre, text=temp_df['percentage'].apply(lambda x: '{0:1.1f}%'.format(x)))
            bar_plots.update_layout(title_x=0.5, showlegend=True)
            st.plotly_chart(bar_plots, use_container_width=True) 
    

    # this codes the interactive line chart
  
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

