# Top 100 Song Lyrics Visualization

## Overview

This project provides a comprehensive analysis of the lyrics of the top 100 end-of-year songs across six different genres over the past 10 years. The project involves collecting the data for the top songs, processing and cleaning the data, creating visualizations, and building a web application to present the findings in an interactive manner.

## Data Scraping

The data for the top songs was collected by scraping the list from billboard.com using the Beautiful Soup library and the lyrics through the Genius Lyrics API. This process involved making API calls and parsing the HTML responses to extract the relevant information.

## Data Cleaning and Organizing

Once the data was collected, it was processed and cleaned to prepare it for use in the visualizations. The cleaning process involved removing unwanted characters, converting text to lowercase, and removing stop words using the nltk library. The processed data was then stored in a Pandas DataFrame and organized to facilitate the creation of meaningful visualizations.

## Visualizations

The visualizations were created using the Plotly Express library and included bar graphs, word clouds, and line charts. These visualizations provide a comprehensive comparison of the different genres in terms of language and themes and allow users to gain valuable insights into the trends and patterns in the music industry.

## Web Application

The web application was built using Streamlit and provides a user-friendly interface to access the processed data and visualizations. The application enables users to interact with the visualizations, explore the data in more detail, and gain a deeper understanding of the trends and patterns in the music industry.

## Conclusion

This project provides a unique, fun, and interactive way to understand the lyrics of the top 100 songs in various genres over the past 10 years. By leveraging data scraping, cleaning, and visualization techniques, users can gain valuable insights into the common themes and language used in popular songs across different genres. The web application provides a user-friendly interface to access this information and enables a deeper understanding of the trends and patterns in the music industry.
