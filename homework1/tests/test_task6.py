import pathlib
import pytest
from task6 import word_counter

#DATA_DIR = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(__file__).resolve().parents[1]




# The @pytest.mark.parametrize decorator runs the same test function
# multiple times with different sets of inputs and expected outputs.
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("task6_read_me.txt", 104),
    ],
)
def test_word_count_for_given_file(filename, expected):
    path = ROOT / filename
    assert word_counter(path) == expected

# Pytest will generate one test case for each tuple in the list below.
@pytest.mark.parametrize(
    "content, expected",
    [
        ("", 0),
        ("one", 1),
        ("two  words", 2),
        ("three\nwords here", 3),
        ("  leading and   multiple   spaces  ", 4),
    ],
)
def test_word_count_various_small_cases(tmp_path, content, expected):
    fp = tmp_path / "tiny.txt"
    fp.write_text(content, encoding="utf-8")
    assert word_counter(fp) == expected
