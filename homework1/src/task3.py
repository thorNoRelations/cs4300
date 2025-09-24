def is_positive(n: int) -> str:
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


#########################

# prime check 
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

#create first n primes 
def first_n_primes(n: int) -> list[int]:
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

# print primes 
def print_first_n_primes(n: int) -> None:

    for prime in first_n_primes(n):
        print(prime)

#################################################
def sum_of_one_hundred():
    n = 1
    total = 0
    while n <= 100:  
        total = total + n
        n = n + 1
    return total