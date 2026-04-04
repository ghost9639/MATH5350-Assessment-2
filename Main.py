"""
Main project file for MATH5350 Assessment 2

Functions are implemented in their own subheadings below in order. All function calls and outputs in
the reports are given in a __main__ function at the bottom of the file with seeds taken before every
disconnected function call.

Project pip dependencies are numpy and matplotlib.
"""

import numpy as np
from numba import jit
from numba import njit
import matplotlib.pyplot as plt
import time
from matplotlib import cbook, cm
from matplotlib.colors import LightSource
import warnings
warnings.filterwarnings("error")


# ===============================================
# Question 1 
# ===============================================

def input_data(S_0, r, mu, sigma, t0, T, K, E, N, M):
    """Input Validation Function

    Returns True when inputs are valid and False otherwise. Expects an initial stock price (S_0) as a positive
    integer or float, an interest rate (r) as a non-negative integer or float, a drift term (mu) as an integer
    or float that must be equal to r to prevent arbitrage, a volatility term (sigma) that must be a non-negative
    integer or float, a starting time (t0) that must be a positive integer or float, the duration of the
    derivative (T) which must be a non-negative number, a strike price (K) that must be a non-negative integer or
    float, a shout price (E) that must be a non-negative integer or float, a number of time splits (N) to
    approximate the continuous time interval which must be a non-negative integer or float, and a sampling
    number (M) that must be a non-negative integer or float.

    Returns True when all inputs are passable and False otherwise."""

    _fail = False               # fail condition allows for check and inverted result can be passed out

    if not (isinstance (S_0, (int, float)) and not isinstance (S_0, bool)) or S_0 <= 0:
        print("Initial stock value must be a positive real number,")
        _fail = True
    
    if not (isinstance (r, (int, float)) and not isinstance (r, bool)) or r <= 0:
        print("The interest rate must be a positive real number,")
        _fail = True

    if not (isinstance (mu, (int, float)) and not isinstance (mu, bool)):
        print("Drift factor must be a number,")
        _fail = True

    if not (isinstance (sigma, (int, float)) and not isinstance (sigma, bool)) or sigma <= 0:
        print("Stock variability must be a positive real number,")
        _fail = True

    if not (isinstance (t0, (int, float)) and not isinstance (t0, bool)) or t0 < 0:
        print("Initial time must be greater than 0,")
        _fail = True

    if not (isinstance (T, (int, float)) and not isinstance (T, bool)) or T <= 0:
        print("Maturity date must be some time in the future,")
        _fail = True

    if not (isinstance (K, (int, float)) and not isinstance (K, bool)) or K <= 0:
        print("The strike price must be a positive number,")
        _fail = True
    
    if not (isinstance (E, (int, float)) and not isinstance (E, bool)) or E <= 0:
        print("The shout price must be a positive number,")
        _fail = True    

    if not (isinstance (N, int) and not isinstance (N, bool)) or N <= 0:
        print("The time steps must be a positive natural number,")
        _fail = True        

    if not (isinstance (M, int) and not isinstance (M, bool)) or M <= 0:
        print("Number of samples must be a positive natural number,")
        _fail = True

    # if mu != r:
    #     print("Model has arbitrage: mu must be equal to r,")  # changed for Question 3
    #     _fail = True

    return not _fail
    
# ===============================================
# Question 2
# ===============================================


def price_euler (S_0, mu, sigma, t0, T, N):
    """Uses basic implementation of Euler-Maruyama method to solve SDEs.

    Expects Initial Stock price (S_0), drift term (mu), volatility (sigma), initial time (t),
    time till maturity (T), the number of time splits (N).
    Returns a path of stock prices as a simple Python list."""

    try:
        assert input_data (S_0, mu, mu, sigma, t0, T, 100, 100, 100, 100)
    except AssertionError:
        print("Please adjust listed inputs.")
        return None
    
    # base set of variables 
    delta_t = T / N
    time_space = [0 for i in range (N+1)] # time interval 
    S = [S_0 for i in range (N+1)]

    for i in range (N): 
        psi = np.random.normal(0, 1) # random walk samples
        time_space[i+1] = time_space[i] + np.sqrt(delta_t) * psi

    for i in range (N):
        t_i = t0 + i * delta_t
        S[i+1] = (S[i] +        # Euler-Maruyama equation
                  mu * S[i] * delta_t +
                  (sigma * S[i] * (1 + 0.9 * np.sin(2 * np.pi * t_i))) * (time_space[i+1] - time_space[i]))
    
    return S


def price_euler_mc (S_0, mu, sigma, t0, T, N, M, seed = None, init_dW = None):
    """`numpy` accelerated Euler-Maruyama function

    Expects Initial Stock price (S_0), drift term (mu), volatility (sigma), initial time (t),
    time till maturity (T), the number of time splits (N), and a number of times to sample (M)
    
    Returns a matrix of possible stock price paths as numpy arrays."""

    try: 
        assert input_data (S_0, mu, mu, sigma, t0, T, 100, 100, N, M)
    except AssertionError:
        print("Please adjust listed inputs.")
        return None
    
    dt = T / N
    t = np.linspace(t0, t0+T, N+1) # linspace creates an array between two bounds with N subdivisions
    
    # Multidimensional Weiner Process

    # ========== INTERNAL STUFF ==============
    if init_dW is not None: # testing version for direct randomness preservation to exact values
        M_cont, N_cont = init_dW.shape
        m = N_cont // N         
        dW = init_dW.reshape(M, N, m).sum(axis=2)
    elif seed is not None:
        np.random.seed(seed)
        dW = np.sqrt(dt) * np.random.normal (size = (M, N)) # basic version, just make N values
    # ========== INTERNAL STUFF ==============

    # path the program usually takes
    else:
        dW = np.sqrt(dt) * np.random.normal (size = (M, N)) # basic version, just make N values         

    Vega = sigma * (1 + 0.9 * np.sin(2 * np.pi * t[:-1]))

    # we can explicitly declare a stochastic process function
    process = 1 + mu * dt + Vega[None,:] * dW

    S_approx = np.zeros((M, N+1))
    S_approx[:, 0] = S_0
    S_approx[:, 1:] = S_0 * np.cumprod(process, axis = 1) # cumprod evaluates the process cumulatively without for loops 

    return S_approx

@njit
def price_euler_mc_numba (S_0, mu, sigma, t0, T, N, M):
    """Alternative numba accelerated version using python for loops for ease of reading

    Expects an initial price S_0, a drift term mu, an initial time t0, a duration T,
    a chain count N, and a sampling number of M. Returns a numpy array. Does not validate
    inputs to avoid numba compiling in object mode."""

    dt = T / N
    S = np.zeros ((M, N+1))
    
    for i in range (M):         # sample
        S[i,0] = S_0
        for j in range (N):     # chain
            dW = np.sqrt(dt) * np.random.normal()
            S[i, j+1] = S[i, j] * (1 + mu * dt + sigma * dW)

    return S


def timing_EM_functions (S_0, mu, sigma, t0, T):  
    """Performance testing function for Question 2

    Uses the Python time library to benchmark the EM function. Expects Initial Stock price (S_0),
    drift term (mu), volatility (sigma), initial time (t), time till maturity (T).
    Contains its own testing sets for different N and M values, times base and numpy versions of
    Euler-Maruyama functions for M repetitions with N time splits (as well as user inputs).
    
    Returns internal testing arrays (N first) and time taken for both functions (base first).
    This function can be extremely slow depending on the inputs for the exact calculation
    function."""

    n_testing = np.array([10, 100, 1000, 10_000]) # We'll use these as discrete times 
    M_testing = np.array([10, 100, 1000, 10_000]) # We'll use these as sampling numbers

    times_1 = np.zeros((len(n_testing), len(M_testing)))                           # holds base speeds 
    times_2 = np.zeros((len(n_testing), len(M_testing)))                           # holds numpy speeds 
    
    for i, n in enumerate (n_testing): # lets us track index and value quickly
        for j, reps in enumerate (M_testing):
            
            # base function testing
            start_time = time.perf_counter()

            for temp in range(reps): # repeat M times
                price_euler (S_0, mu, sigma, t0, T, n) # tests how long M iterations with N splits of base func takes

            end_time = time.perf_counter()
            times_1[i,j] = end_time - start_time 
            
            
            # np function testing 

            start_time = time.perf_counter()
            price_euler_mc (S_0, mu, sigma, t0, T, n, reps)
            end_time = time.perf_counter()
            times_2[i,j] = end_time - start_time 
        
    return n_testing, M_testing, times_1, times_2

def plotting_3d_efficiency (n_testing, M_testing, times_1, times_2, _logged_plot = True, _is_logged = False): 
    """Utility for plotting the computational complexity of two given datasets with known lists of
    iterations and time splits.

    Expects direct output of timing_EM_functions, returns no values but generates 3d plot of time
    complexity against time splits and sampling."""

    _x, _y = np.meshgrid(n_testing, M_testing, indexing="ij", copy=True)

    # If the user wants a _logged_plot (default is true) and the data isn't already logged
    # function assumes _is_logged False means everything is unlogged and True means everything logged
    # timer function just returns raw data in all cases so default should always just work 
    if _logged_plot and not _is_logged:    
        try:
            _x = np.log(_x)
            _y = np.log(_y)
            t_1 = np.log(times_1)
            t_2 = np.log(times_2)

        # numpy preserved all of my time values as greater than 0, but minor exception handling for logs anyway
        except RuntimeWarning:
            _x, _y = np.meshgrid(n_testing, M_testing, indexing="ij", copy=True)            
            _x = np.log(_x + 1e-12)
            _y = np.log(_y + 1e-12)
            t_1 = np.log(times_1 + 1e-12)
            t_2 = np.log(times_2 + 1e-12) 

        except RuntimeError:    
            print("Have you entered negative or already logged values into this function?"
                  + " Please either pass every raw value from timing_EM_functions or log them"
                  + " all yourself and pass _is_logged = True, otherwise you can set _logged_plot"
                  + " to false to prevent any mathematical transformations in function.")
            return None
    else:
        t_1 = times_1
        t_2 = times_2

    # Plot declaration 
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    # 3d colour mapping
    ls = LightSource(270, 300)
    rgb = ls.shade(np.log(times_1 + 1e-12), cmap=cm.gnuplot2, vert_exag=0.1, blend_mode='soft')
    surf = ax1.plot_surface(_x, _y, t_1, rstride=1, cstride=1, facecolors=rgb, 
                            linewidth=0, antialiased=False, shade=False)


    rgb = ls.shade(np.log(times_2 + 1e-12), cmap=cm.gnuplot2, vert_exag=0.1, blend_mode='soft')
    surf = ax2.plot_surface(_x, _y, t_2, rstride=1, cstride=1, facecolors=rgb,
                            linewidth=0, antialiased=False, shade=False) # is this useless?


    # labels and axis management
    ax1.set_xlabel("Time Splits (N)")
    ax1.set_ylabel("Monte Carlo Repetitions (M)")
    ax1.invert_xaxis()
    ax1.set_zlabel("Time Taken (seconds)")

    ax2.set_xlabel("Time Splits (N)")
    ax2.set_ylabel("Monte Carlo Repetitions (M)")
    ax2.invert_xaxis()
    ax2.set_zlabel("Time Taken (seconds)")

    if _logged_plot:
        ax1.set_title("Logged Base Function Time Complexity")
        ax2.set_title("Logged Numpy Function Time Complexity")
    else:
        ax1.set_title("Base Function Time Complexity")
        ax2.set_title("Numpy Function Time Complexity")

        
    plt.show()

def exact_function (S_0, mu, sigma, t0, T, N_cont = 100_000, M = 500, seed = None, init_dW = None):   
    """Utility for experimental function expectations according to exact equation.

    Takes in S_0 as the initial stock price, mu is the drift term, sigma is the stock variability,
    t0 is the initial stock price, T is the length of time till derivative maturity, the time splits
    on the `discrete` time interval (N_discrete), the time splits on the `continuous` time interval (N_cont),
    a seeded value (seed), and a boolean _exact_only value.

    Internal utility for the error calculator and visualiser: does not validate own
    inputs, will return compiler errors in the presence of misinputs.

    Returns exact path and time interval."""
    

    try:
        assert input_data(S_0, mu, mu, sigma, t0, T, 100, 100, M, N_cont)
        assert N_cont > 10_000
    except AssertionError:
        if N_cont < 10_000:
            print("Continuous time splits must exceed 10,000 at least,"
                  + f" interval splits (currently {N_cont})")
        print("Please amend listed errors.")
        return None 

    dt_cont = T / N_cont        # "continuous" interval used for exact rates (should be more granular)
    t_cont = np.linspace(t0, t0+T, N_cont+1)


    if init_dW is not None: 
        dW_cont = init_dW       # this is the usual path, allows both exact calculation and an approximation 
                                # to use the same Brownian motion trajectory
    elif seed is not None:
        np.random.seed(seed)

    else:
        dW_cont = np.sqrt(dt_cont) * np.random.normal (size = (M, N_cont))
        

    # we can now emplace the known Brownian motion path into the exact solution

    volatility_f = sigma * (1 + 0.9 * np.sin(2 * np.pi * t_cont[:-1])) # volatility function of our SDE 

    def F(t):                   # returns analytic solution to stochastic term integral
        """Local seasonal volatility integration function"""
        return (1.405 * t
                + (0.9 / np.pi) * (1 - np.cos(2 * np.pi * t))
                - (0.81 / (8 * np.pi)) * np.sin(4 * np.pi * t))

    # approximates the exact SDE into the deterministic dt integral and the stochastic dW integral 
    dt_integral = mu * (t_cont - t0) - 0.5 * sigma ** 2 * (F(t_cont) - F(t0))

    dW_integral = np.zeros((M, N_cont+1))
    dW_integral[:,1:] = np.cumsum(volatility_f[None,:] * dW_cont, axis=1) # same numpy implicit cumulative loop as before
    # loops over integrals as sum using Reimann integral defn. (this does require a high N_cont to be accurate)

    S_exact = S_0 * np.exp(dt_integral[None,:] + dW_integral) # exact determination of integrals on lognormal style

    return S_exact, t_cont

def function_variability_quantified (S_0, mu, sigma, t0, T, N_cont = 100_000, M = 500):
    """Utility for quantifying distance between EM approximation and exact equation

    Expects the initial stock price (S_0), a drift term (mu), volatility (sigma), the initial time (t0),
    time till maturity (T), continuous time splits (N_cont). Uses the same Brownian motion path for both.
    Returns the test array, a matrix of Euclidean distances between paths, and a matrix of Euclidean 
    distances between the final prices.""" # why does this work now?

    N = np.array([10, 50, 250, 1_250, 6_250], dtype=int) # test timesplit count
    
    try:
        assert input_data(S_0, mu, mu, sigma, t0, T, 100, 100, 100, 100) # basic block to catch misinputs
        assert N_cont > max(N)  # checks continuous value bigger than all others
        assert np.sum(N_cont % N) == 0 # checks all test values divide N_continuous exactly
    except AssertionError:
        if N_cont < max(N):
            print("Continuous time indexing must be greater than largest discrete time approximation,")
        if np.sum(N_cont % N) != 0:
            print(f"The continuous time index must be an exact multiple of all test values: ({N})")
        print("Invalid data inputted, please amend listed entries.")
        return None

    path_err = np.zeros(len(N))         # this holds the Euclidean distances between the approx paths and exact ones
    terminal_err = np.zeros(len(N))     # this holds the norm between the final values between the approx paths and ""

    dt_cont = T / N_cont
    dW_cont = np.sqrt(dt_cont) * np.random.normal (size=(M, N_cont))
                                                                        
    for i, n_splits in enumerate(N):           # we want to try different MC sample levels

        # exact function call 
        S_exact, t_cont = exact_function (S_0, mu, sigma, t0, T, N_cont=N_cont, M=M, init_dW=dW_cont)
        
        # approximate function call

        S_approx = price_euler_mc (S_0, mu, sigma, t0, T, int(n_splits), M, init_dW=dW_cont)


        m = N_cont // n_splits # conversion for exact solution splits to current set

        S_exact_to_approx = S_exact[:,::m] # read all MC chains and every m-th time, same index as the approximation
        

        # Error racked along the path 
        path_err[i] = np.mean(np.abs(S_approx - S_exact_to_approx))

        # Error at the final time
        terminal_err[i] = np.mean(
            np.abs(S_approx[:,-1] - S_exact_to_approx[:,-1]) # same operation just last time row
        )
        
    return N, path_err, terminal_err 


def function_variability_visualiser (S_0, mu, sigma, t0, T, N_discrete = 10_000,
                                     N_cont = 100_000, M = 500, seed = 1234): 
    """Utility for visualising distance between Euler-Maruyama approximation and exact equation

    Expects an initial stock price S_0, a drift term mu, a volatility term sigma, a starting time t0, a
    time till maturity T, and optionally a `discrete` time splitting number N_discrete, a `continuous` time
    splitting number (N_cont), a number of samples M, and a seed (which defaults to 1234).

    Generates a Brownian motion process and runs the EM and exact function path processes for that Brownian
    motion vector. This is then fed into the exact function and Euler-Maruyama functions, allowing a
    direct visual comparison of both under the stochastic process."""

    try:
        assert input_data(S_0, mu, mu, sigma, t0, T, 100, 100, 100, 100) # basic block to catch misinputs
    except AssertionError:
        print("Invalid data inputted, please amend listed entries")
    except TypeError:
        print("Invalid number of inputs?")

    if seed is not None:
        np.random.seed(seed)

    dt_cont = T / N_cont
    dW_cont = np.sqrt(dt_cont) * np.random.normal (size = (M, N_cont)) # brownian motion process 

    # exact function call 
    S_exact, t_cont = exact_function(S_0, mu, sigma, t0, T, N_cont, M, seed, init_dW = dW_cont)
    S_exact = np.mean(S_exact, axis=0)
    
    # approximate function call 
    S_approx = price_euler_mc (S_0, mu, sigma, t0, T, N_discrete, M, init_dW = dW_cont)
    S_approx = np.mean(S_approx, axis=0)
    disc_times = np.linspace(t0, T+t0, N_discrete+1)

    #plot 
    plt.figure(figsize=(10, 6))
    plt.plot(t_cont, S_exact, label="Exact solution", color = "blue", linestyle="--") # put the disc time over the 
    plt.plot(disc_times, S_approx, label=f"Euler-Maruyama ({N_discrete} splits and {M} iterations)",
             color = "red", linestyle="-.") # continuous since it looks too noisy otherwise
    plt.xlabel("Time Interval")
    plt.ylabel("Stock Price Evolution")
    plt.title("EM Approximation vs Exact Solution")
    plt.legend()
    plt.grid(True)
    plt.show()


def EM_accuracy_plot ():
    """Utility for absolute error printing

    Takes in absolute path error and absolute terminal error from function_variability_quantified, and prints
    a stacked bar plot of the values."""

    np.random.seed(1234)
    n, path_err, term_err = function_variability_quantified (100, 0.05, 0.2, 0.0, 1)

    errors = {
        "Path Error": path_err,
        "Terminal Error": term_err,
    }
    
    fig, ax = plt.subplots()
    _x = np.array(n, dtype=str) # np.arange(len(n))
    bottom = np.zeros(len(n), dtype=np.float16)

    for lab, val in errors.items():
        p = ax.bar(_x, val, 0.5, label=lab, bottom=bottom)
        bottom += val

    ax.set_ylabel("Absolute Error (Euclidean norm)")
    ax.set_xlabel("Number of time-splits")
    ax.set_title("Absolute Error across time split values")
    ax.legend(loc="upper right")

    plt.show()

    

# ===============================================
# Question 3
# ===============================================

def price_rk_mc (S_0, mu, sigma, t0, T, N, M):
    """Approximates the price process for the Seasonal Volatility Model SDE using
    the Runge-Kutta scheme.

    Expects an initial stock price (S_0), a drift term (mu), a volatility term (sigma), an initial
    time (t0), a time till maturity (T), a number of time splits (N), and a number of samples (M)
    Returns an array of stock price paths."""

    dt = T / N
    t = np.linspace(t0, t0+T, N+1) # linspace creates an array between two bounds with N subdivisions

    S = np.zeros((M, N+1)) # M is the sample chain, N is the time period
    S[:,0] = S_0

    for i in range (N):         # forced to use for loop due to nested S_hat recurrence relation 
        
        dW = np.sqrt(dt) * np.random.normal (size = M) # numpy can implicitly format the scaled z-samples as a vector

        # we can calculate variables early for ease of reading
        a = S[:,i] * mu
        Vega = sigma * (1 + 0.9 * np.sin(2 * np.pi * t[i])) # volatility function (only of t)
        
        b = S[:,i] * Vega 

        # correction term 
        S_hat = S[:,i] + a * dt + b * np.sqrt(dt)
        b_hat = S_hat * Vega

        
        # RK equation 
        S[:,i+1] = (S[:,i]
                    + a * dt
                    + b * dW
                    + ((b_hat - b) / (2 * np.sqrt(dt))) * (dW ** 2 - dt))
    
    return S

def rk_means_testing (seed = 1234, test_means = [-0.5, -0.2, 0.005, 0.01, 0.02, 0.5, 0.8]):
    """Means testing utility for the Runge-Kutta function in Question 3.

    Expects a seed and vector of potential mu values. Creates a plot of prices."""

    prices = []

    if seed is not None and isinstance(seed, (int, float)):
        np.random.seed(seed)
    
    for i, mu in enumerate(test_means):
        rk_paths = price_rk_mc (100, mu, 0.2, 0, 1.5, 10_000, 500)
        rk_price = np.mean(rk_paths[:,-1])
        prices.append(rk_price)
    
    rk_estimates = {
        "Runge-Kutta Price Estimates": prices,
    }
    
    fig, ax = plt.subplots()
    _x = np.array(test_means, dtype=str) # np.arange(len(n))
    bottom = np.zeros(len(_x), dtype=np.float16)

    for lab, val in rk_estimates.items():
        p = ax.bar(_x, val, 0.5, label=lab, bottom=bottom)
        bottom += val

    ax.set_ylabel("Price of Option")
    ax.set_xlabel("Value of mu")
    ax.set_title("Option prices across values of mu")
    # ax.legend(loc="upper right")

    plt.show()


# ===============================================
# Question 4 
# ===============================================

def shout_price_rk_mc (S_0, r, mu, sigma, t0, T, K, E, N, M, _full_return = False):   
    """Approximates the price process for the Seasonal Volatility Model SDE using
    the Runge-Kutta scheme.

    Expects an initial stock price (S_0), a drift term (mu), a volatility term (sigma), an initial
    time (t0), a time till maturity (T), the strike price (K), the shout price (E), a number of time
    splits (N), a number of samples (M), and a debug command for bigger value returns (_full_return)
    Returns an array of stock price paths."""

    try:
        assert input_data(S_0, r, mu, sigma, t0, T, K, E, N, M)
    except AssertionError:
        print("Please amend listed errors.")
        return None 

    dt = T / N
    t = np.linspace(t0, t0+T, N+1) # linspace creates an array between two bounds with N subdivisions

    current_S = np.full(M, S_0, dtype=np.float64) # vector of "S_{n-1}" values
    
    shouted = np.zeros (M, dtype=bool) # tagged shouts
    locked = np.zeros (M, dtype=np.float64)  # bagged shouts 
    shout_index = np.full (M, -1, dtype=int) # house shouts

    paths = np.zeros ((M, N+1)) # actual path 
    paths[:,0] = S_0 
    
    for i in range (N):         # forced to use for loop due to nested S_hat recurrence relation 
        
        dW = np.sqrt(dt) * np.random.normal (size = M) # numpy can implicitly format the scaled z-samples as a vector

        # S[S[:,:]>=(E,t0)] # slicing for options below shout price since they close above shout price?
        
        # we can calculate variables early for ease of reading
        a = current_S * r
        Vega = sigma * (1 + 0.9 * np.sin(2 * np.pi * t[i])) # volatility function (only of t)
        
        b = current_S * Vega 
        
        # correction term 
        S_hat = current_S + a * dt + b * np.sqrt(dt)
        b_hat = S_hat * Vega

        
        # RK equation 
        S_n = (current_S + a * dt
               + b * dW
               + ((b_hat - b) / (2 * np.sqrt(dt))) * (dW ** 2 - dt))

        new_shouts = (~shouted) & (S_n >= E) # ~ bitflip operator, faster "not" in this case

        if np.any (new_shouts):
            locked[new_shouts] = np.maximum (S_n[new_shouts] - K, 0) # calculate the final payoff for shouters
            shout_index[new_shouts] = i+1 # index new shouters
            shouted[new_shouts] = True    # tag new shouters

        current_S = S_n                # pop old and push new stack onto current S
        paths[:,i+1] = current_S       # push new S onto next path
        
    # final payoffs calculations 
    final_pay = np.maximum (current_S - K, 0) 
    payoffs = np.maximum (final_pay, locked)
    
    disc_rat = np.exp(-r * T)

    # Monte-Carlo moment calculations 
    price = disc_rat * np.mean(payoffs)
    std_err = disc_rat * np.std(payoffs, ddof=1) / np.sqrt(M)

    # debug return with full path for visualisation 
    if _full_return:
        return price, std_err, paths, shouted, shout_index

    # standard return with MC moments only
    return price, std_err 


# ===============================================
# Question 5
# ===============================================

def antithetic_shout_price_rk_mc (S_0, r, mu, sigma, t0, T, K, E, N, M, _full_return = False): 
    """A function that implements the Runge-Kutta model to price a shout call option using Monte Carlo sampling
    and antithetic variables.

    Accepts an initial stock value (S_0), an interest rate (r), a drift term (mu), volatility (sigma), an
    initial time (t0), the duration of the option (T), a strike price (K), a shout price (E), a discrete
    time splitting number (N), how many times to sample (M), and whether the user wants the full debug return
    (_full_return). Sampling must be even for antithetic variable method to work.
    Returns the price and standard error.
    """
    
    try: 
        assert input_data(S_0, r, mu, sigma, t0, T, K, E, N, M)
        assert M % 2 == 0
    except AssertionError:
        if M % 2 != 0:
            print("M must be even for antithetic estimation,")
        print("Please amend listed errors.")
        return None 

    dt = T / N
    t = np.linspace(t0, t0+T, N+1) # linspace creates an array between two bounds with N subdivisions

    current_S = np.full(M, S_0, dtype=np.float64) # vector of "S_{n-1}" values
    
    shouted = np.zeros (M, dtype=bool) # tagged shouts
    locked = np.zeros (M, dtype=np.float64)  # bagged shouts 
    shout_index = np.full (M, -1, dtype=int) # housed shouts

    paths = np.zeros ((M, N+1), dtype=np.float64) # actual path 
    paths[:,0] = S_0

    half = M // 2
    
    for i in range (N):         # forced to use for loop due to nested S_hat recurrence relation 
        
        dW_half = np.sqrt(dt) * np.random.normal (size = half) # positive and negative halves for antithetic
        # dW = np.vstack([dW_half, -dW_half])[:M]                     # vstack vertically aligns two arrays
        dW = np.concatenate([dW_half, -dW_half])

        
        # we can calculate variables early for ease of reading
        a = current_S * r                                   # r over mu to avoid arbitrage, as per Q3
        Vega = sigma * (1 + 0.9 * np.sin(2 * np.pi * t[i])) # volatility function (only of t)
        
        b = current_S * Vega
        
        # correction term 
        S_hat = current_S + a * dt + b * np.sqrt(dt)
        b_hat = S_hat * Vega

        
        # RK equation 
        S_n = (current_S
               + a * dt
               + b * dW
               + ((b_hat - b) / (2 * np.sqrt(dt))) * (dW ** 2 - dt))

        new_shouts = (~shouted) & (S_n >= E) # ~ bitflip operator, faster "not" in this case

        if np.any (new_shouts):
            locked[new_shouts] = np.maximum (S_n[new_shouts] - K, 0) # calculate the final payoff for shouters
            shout_index[new_shouts] = i+1 # index new shouters
            shouted[new_shouts] = True    # tag new shouters

        current_S = S_n                # pop old and push new stack onto current S
        paths[:,i+1] = current_S       # push new S onto next path
        
    # final payoffs calculations 
    final_pay = np.maximum (current_S - K, 0) 
    payoffs = np.maximum (final_pay, locked)

    paired_payoffs = 0.5 * (payoffs[:half] + payoffs[half:]) # takes expectation for value process
    
    disc_rat = np.exp(-r * T)

    # Monte-Carlo mean moment calculations 
    price = disc_rat * np.mean(paired_payoffs)
    std_err = disc_rat * np.std(paired_payoffs, ddof=1) / np.sqrt(half)

    # debug return with full path for visualisation 
    if _full_return:
        return price, std_err, paths, shouted, shout_index

    # standard return with MC moments only
    return price, std_err 


def error_plot (CI = 1.96, S_0 = 100, r = 0.005, mu = 0.005, sigma = np.sqrt(2*0.005),
                t0 = 0, T = 1.5, K = 100, E = 110, N = 10_000, M = 500):
    
    X, v = shout_price_rk_mc (S_0, r, mu, sigma, t0, T, K, E, N, M)
    
    X_a, v_a = antithetic_shout_price_rk_mc (S_0, r, mu, sigma, t0, T, K, E, N, M)

    labs = ["Base Model", "Antithetic Sampling"]
    base_CI = np.array([X-v, X+v]) * CI
    anthetic_CI = np.array([X_a-v_a, X_a+v_a]) * CI 

    means = np.array([X, X_a])
    vars = np.array([v, v_a]) * CI
    
    y = np.arange(len(labs))

    plt.figure (figsize=(12,5))
    plt.errorbar(
        means, y,
        xerr=vars,
        fmt="o",
        capsize=6,
        linewidth=2
    )

    print(means)

    plt.yticks(y,labs)
    plt.xlabel("Option Price")
    plt.title(f"{CI}% confidence interval Monte Carlo shout price")
    plt.grid(axis="x", linestyle = "--", alpha = 0.5)
    plt.show()

    
# ===============================================
# Main
# ===============================================
    
if __name__ == "__main__":

    # =======================================
    # Question 1
    
    # Easily tested with case list like

    invalid_args = [
        [-4, 0.005, 0.005, np.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # S_0 can't be negative
        [True, 0.005, 0.005, np.sqrt(2 * 0.005), 0, 1.5, 100, 110, 5, 1000], # S_0 cannot be boolean
    ]

    try: 
        for arg in invalid_args: 
            assert not input_data(*arg) # outputs "stock value must be ..." twice
    except AssertionError:
        print("Function falsely rejects valid inputs.")
    except TypeError:
        print("Test list contains different number of inputs to test function.")

    # and simply assert (true) in valid cases
    # current validation logic makes checks like whether inputs are acceptable inputs (generally int or float)
    # as well as an arbitrage free check (mu == r), value checks like volatility being positive included also
    # if-else statements attempt to echo meaningful error messages to the user, and no try-catch statements are
    # used since there are no calculations undertaken (no potential for value error)

    # =======================================
    # Question 2

    # Proceeding in order of the report, first, we have the visualisation for the base model
    # seed used for reproducibility 

    # we can run this with t0 = 0.0 first
    np.random.seed(1234)
    ex = price_euler (100, 0.005, 0.005, 0.0, 1.5, 10000)
    plt.figure(figsize=(10, 6))    
    plt.plot (ex)               # plt happy to create x on the fly
    plt.xlabel ("Time")
    plt.ylabel ("Value")
    plt.title ("Potential Projection of Seasonal Volatility Model")
    plt.show()

    # and then with t0 = 0.5
    np.random.seed(1234)
    ex = price_euler (100, 0.005, 0.005, 0.5, 1.5, 10000)
    plt.figure(figsize=(10, 6))    
    plt.plot (ex)               # plt happy to create x on the fly
    plt.xlabel ("Time")
    plt.ylabel ("Value")
    plt.title ("Potential Projection of Seasonal Volatility Model")
    plt.show()


    # with numbas
    np.random.seed(1234)
    ex = price_euler_mc_numba (100, 0.005, 0.005, 0.0, 1.5, 1, 100)
    plt.figure(figsize=(10, 6))    
    plt.plot (ex)               # plt happy to create x on the fly
    plt.xlabel ("Time")
    plt.ylabel ("Value")
    plt.title ("Numba Projection of Seasonal Volatility Model")
    plt.show()
    


    # For the graph of time taken against N and M, bear in mind that it is an operation that will take
    # several minutes, I've left it commented out here but you can try to replicate it if you really want to 

    # n_t, M_t, t_1, t_2 = timing_EM_functions(100, 0.005, 0.005, 0, 1.5)    

    # plotting_3d_efficiency(n_t, M_t, t_1, t_2, _logged_plot=False)        
    # plotting_3d_efficiency(n_t, M_t, t_1, t_2)        
    

    # We want to have a visual idea of how accuracy changes with N and M

    np.random.seed(1234)    
    function_variability_visualiser (100, 0.05, 0.2, 0.0, 1.0, N_discrete=100, M=100)
    function_variability_visualiser (100, 0.05, 0.2, 0.0, 1.0, N_discrete=10_000, M=1000)


    # Finally, we want to evaluate the distance between the approximation and the exact value as N increases
    # This function returns the Euclidean norm between the paths and final values for a range of N values
    
    np.random.seed(1234)
    EM_accuracy_plot()


    # =======================================    
    # Question 3 

    # We can start by showing the projection still works 

    np.random.seed(1234)
    ex_2 = price_rk_mc (100, 0.005, 0.2, 0, 1.5, 10_000, 1)
    ex_2 = ex_2.mean(axis=0)
    t_2 = np.linspace (0.0, 1.5, 10_001)
    plt.figure(figsize=(10, 6))    
    plt.plot (t_2, ex_2)               # plt happy to create x on the fly
    plt.xlabel ("Time")
    plt.ylabel ("Value")
    plt.title ("Potential Projection of Seasonal Volatility Model")
    plt.show()

    # Prices across different values of mu 
    rk_means_testing()
    

    # =======================================    
    # Question 4

    np.random.seed(1234)
    rk_price, std_err = shout_price_rk_mc(S_0 = 100, r = 0.005, mu = 0.005, sigma = np.sqrt(2*0.005),
                                          t0 = 0.0, T = 1.5, K = 100, E = 110, N = 50_000, M = 1000)

    
    print(f"The price of the option is {rk_price:.3f}, and the 95% confidence intervals are "
          + f"[{rk_price-std_err:.3f}, {rk_price+std_err:.3f}].")

    
    # =======================================    
    # Question 5

    np.random.seed(1234)
    error_plot()
    
