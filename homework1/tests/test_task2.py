from task2 import rand_integers, rand_floats, strings, bools

def test_integers():

    assert isinstance(rand_integers(),int) 

def test_floats():

    assert isinstance(rand_floats(),float)

def test_strings():

    assert isinstance(strings(),str)

def test_boolean():

    assert isinstance(bools(),bool)