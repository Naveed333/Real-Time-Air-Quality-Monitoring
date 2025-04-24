def clean_data(df):
    df = df.dropna()
    df = df[df["value"] > 0]
    return df
