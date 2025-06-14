import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Data Preprocessing 

def load_data(csv_path):
    return pd.read_csv(csv_path)

def parse_column(df, column, key='name'):
    parsed_data = []
    for value in df[column]:
        if pd.notnull(value):
            parsed_items = ast.literal_eval(value)
            names = []
            for item in parsed_items:
                names.append(item[key])
            parsed_data.append(names)
        else:
            parsed_data.append([])
    return pd.Series(parsed_data)

def apply_filters(df, selected_genre, selected_lang):
    if selected_genre:
        genre_filtered = []
        for genres in df['genres_parsed']:
            if any(g in genres for g in selected_genre):
                genre_filtered.append(True)
            else:
                genre_filtered.append(False)
        df = df[genre_filtered]

    if selected_lang:
        lang_filtered = []
        for langs in df['languages_parsed']:
            if any(l in langs for l in selected_lang):
                lang_filtered.append(True)
            else:
                lang_filtered.append(False)
        df = df[lang_filtered]

    return df

# Plotting & Analysis Functions 

def plot_budget_vs_revenue(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df['budget'], df['revenue'], c=df['vote_average'], cmap='winter', alpha=0.7)
    ax.set_xlabel('Budget', color='white')
    ax.set_ylabel('Revenue', color='white')
    ax.set_title('Budget vs Revenue (colored by Vote Average)', color='white')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Vote Average')
    return fig

def top_roi_movies(df):
    df['roi'] = (df['revenue'] - df['budget']) / (df['budget'] + 1)
    high_budget = df[df['budget'] > 1e7]
    sorted_df = high_budget.sort_values(by='roi', ascending=False)
    return sorted_df.head(10)

def plot_genre_distribution(df):
    genre_list = []
    for sublist in df['genres_parsed']:
        for genre in sublist:
            genre_list.append(genre)
    genre_counts = pd.Series(genre_list).value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis", ax=ax)
    ax.set_xlabel("Number of Movies")
    ax.set_ylabel("Genre")
    ax.set_title("Top 15 Genre Counts")
    return fig

def plot_runtime_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['runtime'].dropna(), bins=30, kde=False, color="#00cc96", ax=ax)
    ax.set_xlabel("Runtime (minutes)", color='white')
    ax.set_ylabel("Number of Movies", color='white')
    ax.set_title("Runtime Distribution", color='white')
    return fig

def plot_correlation_heatmap(df):
    num_cols = ['budget', 'revenue', 'popularity', 'vote_average', 'vote_count', 'runtime']
    fig, ax = plt.subplots(figsize=(10, 6))
    correlation_matrix = df[num_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="berlin", ax=ax)
    ax.set_title("Correlation Heatmap (Numerical Features)")
    return fig

def plot_yearly_trend(df):
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
    yearly_counts = df['year'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(yearly_counts.index, yearly_counts.values, marker='o', color='teal')
    ax.set_xlabel("Year", color='white')
    ax.set_ylabel("Movies Released", color='white')
    ax.set_title("Movies Released Over the Years", color='white')
    return fig

def plot_keyword_wordcloud(df):
    all_keywords = []
    for sublist in df['keywords_parsed']:
        all_keywords.extend(sublist)
    keywords_text = ' '.join(all_keywords)

    wordcloud = WordCloud(width=1000, height=500, background_color='black', colormap='plasma').generate(keywords_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig

