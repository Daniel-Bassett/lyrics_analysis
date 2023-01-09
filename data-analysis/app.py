import plotly_express as px
import streamlit as st
import pandas as pd

# load the data
df = pd.read_csv('..\data\lyrics\clean_df.csv')
word_count_df = pd.read_csv('..\data\lyrics\word_count.csv')

def main():
    st.title('Lyrics Analysis')
    st.header('Brief Introduction')
    st.write('placeholder')

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
word = 'beer'
genre = 'Country'
word_count = word_count_df[(word_count_df['genre'] == genre) & (word_count_df['word'] == word)]['count']
country_song_count = len(df[df['genre'] == genre]['title'].unique())
temp_df = word_count_df[(word_count_df['genre'] == genre) & (word_count_df['word'] == word)]
barh_plot = px.bar(y=percentage, orientation='h')

# top 5 words for one genre
top_5 = word_count_df.groupby('genre').head().sort_values(by=['genre', 'count'], ascending=False)
st.dataframe(df)
bar_plots = px.bar(data_frame=top_5[top_5['genre'] == 'Pop'], x='word', y='count')
bar_plots.update_layout(title_x=0.5, showlegend=True)
st.plotly_chart(bar_plots, use_container_width=True)

    # # this plots the scatterplot
    # with st.expander('Avg Rank of Songs Word Appears In vs. Their Song Count'):
    #     top_100_words_mask = new_df['word'].isin(new_df['word'].value_counts().head(200).index)
    #     word_average_rank = new_df[top_100_words_mask].groupby('word')['rank'].agg(['count', 'mean']).reset_index()
    #     scatter_plot = px.scatter(word_average_rank, x='mean', y='count', hover_data=['word'], labels={'mean': 'Average Rank of Song in which Word Appears', 'count': 'Number of Songs Appears In'}, title='Average Rank of Songs a Word Appears in Compared to Song Count')
    #     scatter_plot.update_xaxes(autorange='reversed')
    #     st.plotly_chart(scatter_plot, use_container_width=True)

    

if __name__ == '__main__':
    main()

