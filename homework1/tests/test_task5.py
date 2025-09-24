import pytest
from task5 import favorite_books, get_first_three_books, student_db, get_student_id


def test_favorite_books_structure():
    
    assert len(favorite_books) > 0
   
    for book in favorite_books:
        assert isinstance(book, tuple)
        assert len(book) == 2


def test_first_three_books():

    first_three = get_first_three_books()
    assert len(first_three) == 3
    assert first_three == favorite_books[:3]


def test_student_db_structure():
    
    assert isinstance(student_db, dict)
    assert len(student_db) > 0


def test_get_student_id():

    assert get_student_id("Ripley") == "A001"
    assert get_student_id("Dallas") == "A002"
    assert get_student_id("Xenomorph") is None
