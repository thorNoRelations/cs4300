import random

def rand_integers(low=0, high=100):
    
    return random.randint(low, high)

def rand_floats(low=0.0, high=100.0):
    
    return random.uniform(low, high)

def strings():

    return "string"

import random

def bools():

    x = random.randint(0, 1)  
    z = bool(x)              
    return z