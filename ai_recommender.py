import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("cs_books_dataset.csv")

df["content"] = df["Title"] + " " + df["Subject"]

vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(df["content"])

print("AI Library Book Recommender Ready!")

while True:
    query = input("\nAsk for a book: ")

    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, matrix)

    scores = similarity.flatten()
    top_indices = scores.argsort()[-5:][::-1]

    print("\nRecommended Books:\n")

    for i in top_indices:
        print(df.iloc[i]["Title"], "by", df.iloc[i]["Author"])