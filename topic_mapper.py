TOPIC_MAP = {
    "data structures": {"query": "data structures algorithms", "subject": "computer science", "label": "Data Structures & Algorithms"},
    "dsa": {"query": "data structures algorithms", "subject": "computer science", "label": "Data Structures & Algorithms"},
    "algorithms": {"query": "algorithms design analysis", "subject": "computer science", "label": "Algorithms"},
    "recursion": {"query": "recursion algorithms programming", "subject": "computer science", "label": "Recursion & Algorithms"},
    "sorting": {"query": "sorting algorithms data structures", "subject": "computer science", "label": "Sorting & Algorithms"},
    "trees": {"query": "trees graphs data structures algorithms", "subject": "computer science", "label": "Trees & Graphs"},
    "graphs": {"query": "graph theory algorithms", "subject": "computer science", "label": "Graph Algorithms"},
    "dynamic programming": {"query": "dynamic programming algorithms", "subject": "computer science", "label": "Dynamic Programming"},
    "dp": {"query": "dynamic programming algorithms", "subject": "computer science", "label": "Dynamic Programming"},
    "database": {"query": "database management systems", "subject": "databases", "label": "Database Management"},
    "dbms": {"query": "database management systems SQL", "subject": "databases", "label": "DBMS"},
    "sql": {"query": "SQL database programming", "subject": "databases", "label": "SQL & Databases"},
    "normalization": {"query": "database normalization DBMS design", "subject": "databases", "label": "Database Normalization"},
    "er diagram": {"query": "entity relationship database design", "subject": "databases", "label": "Database Design"},
    "nosql": {"query": "NoSQL MongoDB database", "subject": "databases", "label": "NoSQL Databases"},
    "python": {"query": "python programming", "subject": "python", "label": "Python Programming"},
    "java": {"query": "java programming object oriented", "subject": "java", "label": "Java Programming"},
    "c++": {"query": "c++ programming", "subject": "c++", "label": "C++ Programming"},
    "javascript": {"query": "javascript web development", "subject": "javascript", "label": "JavaScript"},
    "c": {"query": "c programming language", "subject": "computer science", "label": "C Programming"},
    "machine learning": {"query": "machine learning artificial intelligence", "subject": "machine learning", "label": "Machine Learning"},
    "ml": {"query": "machine learning algorithms", "subject": "machine learning", "label": "Machine Learning"},
    "deep learning": {"query": "deep learning neural networks", "subject": "artificial intelligence", "label": "Deep Learning"},
    "artificial intelligence": {"query": "artificial intelligence", "subject": "artificial intelligence", "label": "Artificial Intelligence"},
    "ai": {"query": "artificial intelligence machine learning", "subject": "artificial intelligence", "label": "Artificial Intelligence"},
    "neural networks": {"query": "neural networks deep learning", "subject": "artificial intelligence", "label": "Neural Networks"},
    "nlp": {"query": "natural language processing", "subject": "artificial intelligence", "label": "Natural Language Processing"},
    "computer vision": {"query": "computer vision image processing", "subject": "artificial intelligence", "label": "Computer Vision"},
    "web development": {"query": "web development html css javascript", "subject": "web development", "label": "Web Development"},
    "flask": {"query": "flask python web development", "subject": "python", "label": "Flask & Python Web"},
    "django": {"query": "django python web framework", "subject": "python", "label": "Django"},
    "operating systems": {"query": "operating systems process memory", "subject": "operating systems", "label": "Operating Systems"},
    "os": {"query": "operating systems linux", "subject": "operating systems", "label": "Operating Systems"},
    "networking": {"query": "computer networks protocols", "subject": "computer networks", "label": "Computer Networks"},
    "computer networks": {"query": "computer networks TCP IP", "subject": "computer networks", "label": "Computer Networks"},
    "software engineering": {"query": "software engineering design patterns", "subject": "software engineering", "label": "Software Engineering"},
    "design patterns": {"query": "design patterns software architecture", "subject": "software engineering", "label": "Design Patterns"},
    "oop": {"query": "object oriented programming design", "subject": "computer science", "label": "Object Oriented Programming"},
    "cybersecurity": {"query": "cybersecurity ethical hacking", "subject": "computer security", "label": "Cybersecurity"},
    "cryptography": {"query": "cryptography security algorithms", "subject": "computer security", "label": "Cryptography"},
    "discrete mathematics": {"query": "discrete mathematics computer science", "subject": "mathematics", "label": "Discrete Mathematics"},
    "discrete math": {"query": "discrete mathematics logic proofs", "subject": "mathematics", "label": "Discrete Mathematics"},
    "linear algebra": {"query": "linear algebra machine learning", "subject": "mathematics", "label": "Linear Algebra"},
    "statistics": {"query": "statistics probability data science", "subject": "mathematics", "label": "Statistics"},
    "data science": {"query": "data science python analytics", "subject": "data science", "label": "Data Science"},
    "data analysis": {"query": "data analysis pandas python", "subject": "data science", "label": "Data Analysis"},
    "big data": {"query": "big data hadoop spark", "subject": "data science", "label": "Big Data"},
}

def map_topic(query: str):
    query_lower = query.lower().strip()
    if query_lower in TOPIC_MAP:
        return TOPIC_MAP[query_lower]
    for key, value in TOPIC_MAP.items():
        if key in query_lower or query_lower in key:
            return value
    return {
        "query": f"{query} computer science",
        "subject": "computer science",
        "label": query.title()
    }

def get_all_topics():
    seen = set()
    topics = []
    for val in TOPIC_MAP.values():
        label = val["label"]
        if label not in seen:
            seen.add(label)
            topics.append(label)
    return sorted(topics)