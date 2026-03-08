import requests
import pandas as pd

subjects = [
    "python programming",
    "data structures",
    "algorithms",
    "machine learning",
    "database systems",
    "computer science"
]

books = []

for subject in subjects:
    url = f"https://openlibrary.org/search.json?q={subject}&limit=100"

    response = requests.get(url)
    data = response.json()

    for book in data["docs"]:
        title = book.get("title")
        author = book.get("author_name", ["Unknown"])[0]

        books.append([title, author, subject])

df = pd.DataFrame(books, columns=["Title", "Author", "Subject"])

df.to_csv("cs_books_dataset.csv", index=False)

print("Dataset created successfully!")