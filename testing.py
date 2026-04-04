import pytest
import math

from Main import input_data

# input_data(S_0, r, mu, sigma, t0, T, K, E, N, M)
invalid_args = [ 
    [-4, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # S_0 can't be negative
    [True, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # S_0 cannot be boolean
    ["two hundred", 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # S_0 can't be string
    [0, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # stock can't be free 
    [100, -0.005, -0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # mu and r must be positive
    [100, True, True, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # mu and r can't be booleans
    [100, "Point 5", "Point 5", math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # mu and r cannot be strings
    [100, 0.005, 0.005, -5, 0, 1.5, 100, 110, 5, 1000], # volatility must be positive 
    [100, 0.005, 0.005, 0, 0, 1.5, 100, 110, 5, 1000], # volatility cannot be 0
    [100, 0.005, 0.005, "four", 0, 1.5, 100, 110, 5, 1000], # volatility cannot be a string
    [100, 0.005, 0.005, True, 0, 1.5, 100, 110, 5, 1000],   # volatility cannot be a boolean
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), -5, 1.5, 100, 110, 5, 1000], # starting time probably shouldn't be -ve
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), False, 1.5, 100, 110, 5, 1000], # Starting time shouldn't be bool
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), "Soon", 1.5, 100, 110, 5, 1000], # starting time shouldn't be a string
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, -5, 100, 110, 5, 1000], # TTM can't be negative
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, "Three years", 100, 110, 5, 1000], # TTM can't be str
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, True, 100, 110, 5, 1000], # TTM can't be bool
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, -5, 110, 5, 1000], # K can't be negative
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, True, 110, 5, 1000], # K can't be bool
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, "one hundred", 110, 5, 1000], # K can't be str
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, True, 5, 1000], # shout price can't be a boolean
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, "two hundred", 5, 1000], # shout price not str
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, -1.56, 5, 1000], # shout price not negative
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 0, 1000], # must have at least one measure
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, -5, 1000], # cannot have negative measures
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, True, 1000], # measure not bool
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, "three", 1000], # measure not str
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, -5], # must have positive number of MC iterations
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 0], # must have at least one iteration
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, True], # iteration can't be boolean
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, "40"], # can't have string iterations 
]

valid_args = [
    [100, 0.005, 0.005, math.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000] # N and M are free floating and impact accuracy + cost complexity
]

# ============================================
# Testing input_data
# ============================================

@pytest.mark.parametrize("args", invalid_args)
def test1 (args):
    assert not input_data(*args)

@pytest.mark.parametrize ("args", valid_args)
def test2 (args):
    assert input_data(*args)

    

    
