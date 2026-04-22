import pandas as pd
# Summary stats for artists
def artist_summary(df, artist):

    df = df[df['artists'] == artist]

    return df.describe()[['duration_s', 'energy', 'acousticness', 'tempo']]

def feature_trend(df, feature):
    """
    Average feature value per year.
    """

    df = df.copy()
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    return df.groupby('year')[feature].mean().reset_index()

def top_songs(df, feature, n=10):
    """
    Return top n songs ranked by a given feature.
    """

    df = df.copy()

    # Check column exists
    if feature not in df.columns:
        raise ValueError(f"{feature} is not a valid column")

    # Convert to numeric safely
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Drop missing values
    df = df.dropna(subset=[feature])

    # Remove duplicates (important)
    df = df.drop_duplicates(subset=['name', 'artists'])

    # Sort and select top n
    top = df.sort_values(feature, ascending=False).head(n)

    # Return clean output
    return top[['name', 'artists', feature]]

def artist_variability(df, artist):
    """
    Measure how diverse a specific artist's music is.
    """

    features = ['duration_s', 'energy', 'acousticness', 'tempo', 'valence']

    # Filter to one artist
    df_artist = df[df['artists'] == artist].copy()

    if df_artist.empty:
        raise ValueError("Artist not found in dataset")

    # Ensure numeric
    for col in features:
        df_artist[col] = pd.to_numeric(df_artist[col], errors='coerce')

    df_artist = df_artist.dropna(subset=features)

    # Compute standard deviation per feature
    variability = df_artist[features].std().to_frame().T

    # Add overall score
    variability['overall_variability'] = variability.mean(axis=1)

    return variability

def feature_correlations(df):
    """
    Return correlation matrix for audio features.
    """

    features = ['duration_s', 'energy', 'acousticness', 'tempo', 'valence']

    return df[features].corr()
