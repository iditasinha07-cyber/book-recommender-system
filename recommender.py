from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openlibrary import fetch_books
from topic_mapper import map_topic
import re

def build_book_text(book):
    parts = [
        book.get("title", ""),
        " ".join(book.get("authors", [])),
        " ".join(book.get("subjects", [])),
        book.get("level", "")
    ]
    return " ".join(parts).lower()

def recommend_books(user_query: str, level_filter: str = "All", top_n: int = 5):
    topic_info = map_topic(user_query)
    search_query = topic_info["query"]
    subject = topic_info["subject"]
    topic_label = topic_info["label"]

    books = fetch_books(query=search_query, subject=subject, limit=30)

    if not books:
        return [], topic_label, "No books found. Try a different query."

    if level_filter != "All":
        filtered = [b for b in books if b["level"] == level_filter]
        if len(filtered) >= 3:
            books = filtered

    book_texts = [build_book_text(b) for b in books]
    query_clean = re.sub(r"[^\w\s]", "", user_query.lower())

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(book_texts + [query_clean])
        query_vector = tfidf_matrix[-1]
        book_vectors = tfidf_matrix[:-1]
        scores = cosine_similarity(query_vector, book_vectors).flatten()
        for i, book in enumerate(books):
            book["score"] = round(float(scores[i]), 4)
        ranked = sorted(books, key=lambda x: (x["score"], x.get("rating") or 0), reverse=True)
    except Exception:
        ranked = books

    return ranked[:top_n], topic_label, None

def get_similar_books(book_title: str, top_n: int = 5):
    books = fetch_books(query=book_title, limit=20)
    if not books:
        return []
    book_texts = [build_book_text(b) for b in books]
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(book_texts)
        ref_vector = tfidf_matrix[0]
        scores = cosine_similarity(ref_vector, tfidf_matrix).flatten()
        scores[0] = 0
        for i, book in enumerate(books):
            book["score"] = round(float(scores[i]), 4)
        ranked = sorted(books, key=lambda x: x["score"], reverse=True)
        return ranked[:top_n]
    except Exception:
        return books[1:top_n+1]