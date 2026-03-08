import pandas as pd

df = pd.read_csv("cs_books_dataset.csv")

print("Welcome to the Computer Science Library Recommender")

while True:
    query = input("\nWhat book are you looking for? ")

    results = df[df["Subject"].str.contains(query, case=False, na=False)]

    if len(results) == 0:
        print("No books found. Try another topic.")
    else:
        print("\nRecommended Books:\n")
        for i, row in results.head(5).iterrows():
            print(row["Title"], "by", row["Author"])