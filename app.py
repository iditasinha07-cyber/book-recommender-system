from flask import Flask, render_template, request, jsonify
from recommender import recommend_books, get_similar_books
from topic_mapper import get_all_topics

app = Flask(__name__)

def get_ai_explanation(query, books, topic_label):
    """Generate explanation without Claude API — fully free."""
    if not books:
        return None

    top_book = books[0]
    beginner_book = next((b for b in books if b["level"] == "Beginner"), books[0])

    explanation = (
        f"Based on your search for '{query}', these are the best {topic_label} books "
        f"available on Open Library. '{top_book['title']}' is the highest-ranked result "
        f"based on relevance and rating. "
        f"If you are a complete beginner, start with '{beginner_book['title']}' — "
        f"it matches beginner-level content for this topic. "
        f"Tip: Focus on understanding the core concepts first before jumping into advanced material."
    )
    return explanation


@app.route("/")
def index():
    topics = get_all_topics()
    return render_template("index.html", topics=topics)


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "").strip()
    level = data.get("level", "All")

    if not query:
        return jsonify({"error": "Please enter a search query."}), 400

    books, topic_label, error = recommend_books(query, level_filter=level, top_n=5)

    if error and not books:
        return jsonify({"error": error}), 404

    ai_explanation = get_ai_explanation(query, books, topic_label)

    return jsonify({
        "books": books,
        "topic_label": topic_label,
        "ai_explanation": ai_explanation,
        "query": query,
        "level": level
    })


@app.route("/similar", methods=["POST"])
def similar():
    data = request.get_json()
    book_title = data.get("title", "").strip()

    if not book_title:
        return jsonify({"error": "Book title is required."}), 400

    similar = get_similar_books(book_title, top_n=5)
    return jsonify({"books": similar, "based_on": book_title})


@app.route("/topics")
def topics():
    return jsonify({"topics": get_all_topics()})


if __name__ == "__main__":
    app.run(debug=True)