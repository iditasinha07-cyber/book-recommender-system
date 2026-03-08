from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

df = pd.read_csv("cs_books_dataset.csv")
df["content"] = df["Title"] + " " + df["Subject"]

vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(df["content"])

@app.route("/", methods=["GET", "POST"])
def home():
    books = []

    if request.method == "POST":
        query = request.form["query"]

        query_vec = vectorizer.transform([query])
        similarity = cosine_similarity(query_vec, matrix)

        scores = similarity.flatten()
        top_indices = scores.argsort()[-5:][::-1]

        for i in top_indices:
            books.append(df.iloc[i]["Title"] + " by " + df.iloc[i]["Author"])

    return render_template("index.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)