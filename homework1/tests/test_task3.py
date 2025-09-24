from task3 import is_positive, is_prime, first_n_primes, print_first_n_primes, sum_of_one_hundred

def test_ispositive():

    nums = [1,-0.01, 0]
    expected = ["positive", "negative", "zero"]

    for i in range(len(nums)):
        assert is_positive(nums[i]) == expected[i]

################################################
def test_is_prime_with_primes():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(29)

def test_is_prime_with_non_primes():
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(100)

def test_first_n_primes_length():
    result = first_n_primes(10)
    assert len(result) == 10

def test_first_n_primes_values():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert first_n_primes(10) == expected

def test_first_n_primes_small():
    assert first_n_primes(1) == [2]
    assert first_n_primes(2) == [2, 3]
################################################################

def test_sum_of_one_hundred():
    assert sum_of_one_hundred() == 5050