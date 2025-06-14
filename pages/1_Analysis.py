
import streamlit as st
from utilities import *

st.set_page_config(page_title="Movie EDA", layout="wide")

# Load and preprocess
@st.cache_data
def load_and_preprocess():
    df = load_data(r"C:\Users\Hp\OneDrive\Documents\project\movie_recommender_system\data\tmdb_5000_movies.csv")
    df['genres_parsed'] = parse_column(df, 'genres')
    df['keywords_parsed'] = parse_column(df, 'keywords')
    df['languages_parsed'] = parse_column(df, 'spoken_languages')
    return df

df = load_and_preprocess()
st.title("Exploratory Data Analysis - TMDB 5000 Movies")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_genre = st.sidebar.multiselect("Select Genres", sorted(set(g for sub in df['genres_parsed'] for g in sub)))
selected_lang = st.sidebar.multiselect("Select Languages", sorted(set(l for sub in df['languages_parsed'] for l in sub)))

filtered_df = apply_filters(df.copy(), selected_genre, selected_lang)

# Budget vs Revenue
st.subheader("Revenue vs Budget")
fig1 = plot_budget_vs_revenue(filtered_df)
st.plotly_chart(fig1, use_container_width=True)

# ROI Table
st.subheader("Top 10 Movies by ROI (High Budget Only)")
roi_df = top_roi_movies(filtered_df)
st.dataframe(roi_df[['title', 'budget', 'revenue', 'roi']])

# Genre Distribution
st.subheader("Genre Distribution")
fig2 = plot_genre_distribution(filtered_df)
st.pyplot(fig2)

# Runtime Distribution
st.subheader("Runtime Distribution")
fig3 = plot_runtime_distribution(filtered_df)
st.plotly_chart(fig3, use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Heatmap (Numerical Features)")
fig4 = plot_correlation_heatmap(filtered_df)
st.pyplot(fig4)

# Yearly Release Trend
st.subheader("Movies Released Over the Years")
fig6 = plot_yearly_trend(filtered_df)
st.plotly_chart(fig6)

# Keyword Word Cloud
st.subheader("Keywords Word Cloud")
fig7 = plot_keyword_wordcloud(filtered_df)
st.pyplot(fig7)
