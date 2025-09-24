# List of favorite books (title, author)
favorite_books = [
    ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams"),
    ("The Restaurant at the End of the Universe", "Douglas Adams"),
    ("Life, the Universe and Everything", "Douglas Adams"),
    ("So Long, and Thanks for All the Fish", "Douglas Adams"),
    ("Mostly Harmless", "Douglas Adams")
]

# Print the first three books using slicing
def get_first_three_books():
    return favorite_books[:3]


# Dictionary of students
student_db = {
    "Ripley": "A001",
    "Dallas": "A002",
    "Lambert": "A003",
    "Ash": "A004",
    "Kane": "A005",
    "Parker": "A006",
    "Brett": "A007"
}

# Lookup student ID by name
def get_student_id(name):
    return student_db.get(name)
