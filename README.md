
# Table of Contents

1.  [Stochastic Differential Equation (SDE) Solver](#orga4a7cf5)
2.  [Features](#orgbc55d45)
    1.  [Euler-Maruyama (EM) scheme](#orgdb92c13)
    2.  [Function Benchmarking](#orgb645a98)
    3.  [Accuracy Analysis](#org09c38b4)
    4.  [Runge-Kutta (RK) scheme](#org21be1e4)
    5.  [Exotic option pricing](#org91aa583)
    6.  [Unit Testing and Input Validation](#org861563e)
3.  [Installation](#orgb8def5a)
4.  [Project Insights](#org2c7d6f0)
5.  [Potential Improvements](#org337bb89)



<a id="orga4a7cf5"></a>

# Stochastic Differential Equation (SDE) Solver

This project implements a high performance SDE solver. It employs number of approaches towards solving a defined Stochastic Differential Equation modelling a stock price, and later Monte Carlo methods for estimating the price of a Bermudan shout option on the stock. Numpy and Numbas are used for optimal memory and runtime efficiency within Python.

$$d S_t = S_t \mu dt + S_t \sigma [1 + 0.9 \sin (2 \pi t)] d W_t$$

A seasonal volatility model is solved in the [full report](Report.pdf). The [main file](Main.py) and [unit testing](testing.py) files are also available.


<a id="orgbc55d45"></a>

# Features


<a id="orgdb92c13"></a>

## Euler-Maruyama (EM) scheme

1.  Baseline model for comparisons,
2.  Numpy accelerated version,
3.  Numbas accelerated version,


<a id="orgb645a98"></a>

## Function Benchmarking

1.  Performance timing for EM models,
2.  Time complexity across sampling and chains shown on clear 3d pyplot,


<a id="org09c38b4"></a>

## Accuracy Analysis

1.  Exact solution calculated for efficiency estimates,
2.  Errors quantified and visualised,


<a id="org21be1e4"></a>

## Runge-Kutta (RK) scheme

1.  Highly efficient RK scheme implemented in numpy,
2.  Strong and weak convergence for path-dependent options,


<a id="org91aa583"></a>

## Exotic option pricing

1.  Use of numpy accelerated Monte Carlo sampling of RK scheme to price Bermudan shout option,
2.  **Antithetic sampling** for higher efficiency,
3.  Visualisation of paths and convergence,


<a id="org861563e"></a>

## Unit Testing and Input Validation

1.  Use of pytest to ensure edge cases considered,
2.  Input validation function for function safety.


<a id="orgb8def5a"></a>

# Installation

If you have git and pip,

    # download project
    git clone https://github.com/ghost9639/MATH5350-Assessment-2
    cd MATH5350-Assessment-2
    
    # install any required dependencies
    pip install numpy numba matplotlib
    
    # alternatively, if you have nix
    nix-shell


<a id="org2c7d6f0"></a>

# Project Insights

1.  Numpy acceleration and Numba JIT compilation for high efficiency compared to base Python,
2.  Euler-Maruyama is easily debugged but lacks weak convergence for path independent options,
3.  Runge-Kutta scheme has higher computational cost but weak convergence,
4.  Antithetic sampling for faster convergence,


<a id="org337bb89"></a>

# Potential Improvements

1.  GPU acceleration,
2.  Further MC methods,
3.  Support for general and multi-dimensional SDEs,
4.  Calibration for real data.

