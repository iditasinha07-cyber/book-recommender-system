import requests

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"

def fetch_books(query, subject=None, limit=20):
    params = {
        "q": f"{query} computer science",
        "subject": subject or "computer science",
        "fields": "key,title,author_name,subject,first_publish_year,cover_i,edition_count,ia,number_of_pages_median,ratings_average,ratings_count",
        "limit": limit,
        "lang": "eng"
    }
    try:
        response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        books = []
        for doc in data.get("docs", []):
            title = doc.get("title", "Unknown Title")
            authors = doc.get("author_name", ["Unknown Author"])
            subjects = doc.get("subject", [])
            year = doc.get("first_publish_year", "N/A")
            cover_id = doc.get("cover_i")
            pages = doc.get("number_of_pages_median", "N/A")
            rating = doc.get("ratings_average", None)
            rating_count = doc.get("ratings_count", 0)
            ol_key = doc.get("key", "")
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
            ol_url = f"https://openlibrary.org{ol_key}" if ol_key else None
            level = detect_level(subjects, title)
            books.append({
                "title": title,
                "authors": authors[:2],
                "subjects": subjects[:8],
                "year": year,
                "cover_url": cover_url,
                "pages": pages,
                "rating": round(rating, 1) if rating else None,
                "rating_count": rating_count,
                "ol_url": ol_url,
                "level": level
            })
        return books
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

def detect_level(subjects, title):
    text = " ".join(subjects).lower() + " " + title.lower()
    if any(word in text for word in ["beginner", "introduction", "intro", "basic", "fundamentals", "learn", "getting started", "crash course", "for dummies", "primer"]):
        return "Beginner"
    elif any(word in text for word in ["advanced", "expert", "mastering", "professional", "deep dive", "in depth", "internals"]):
        return "Advanced"
    else:
        return "Intermediate"