
# Table of Contents

1.  [Stochastic Differential Equation (SDE) Solver](#orgd6b6ed7)
2.  [Features](#org6bf8602)
    1.  [Euler-Maruyama (EM) scheme](#org132b012)
    2.  [Function Benchmarking](#org96fbb8e)
    3.  [Accuracy Analysis](#orge14c460)
    4.  [Runge-Kutta (RK) scheme](#orga2e71ae)
    5.  [Exotic option pricing](#org76c50a0)
    6.  [Unit Testing and Input Validation](#org899e8d3)
3.  [Installation](#org63d1757)
4.  [Project Insights](#orgc03fc9c)
5.  [Potential Improvements](#orgaf401f8)



<a id="orgd6b6ed7"></a>

# Stochastic Differential Equation (SDE) Solver

This project implements a high performance SDE solver. It employs number of approaches towards solving a defined Stochastic Differential Equation modelling a stock price, and later Monte Carlo methods for estimating the price of a Bermudan shout option on the stock. Numpy and Numbas are used for optimal memory and runtime efficiency within Python.

$$d S_t = S_t \mu dt + S_t \sigma [1 + 0.9 \sin (2 \pi t)] d W_t$$

A seasonal volatility model is solved in the [full report](Report.pdf). The [main file](Main.py) and [unit testing](testing.py) files are also available.


<a id="org6bf8602"></a>

# Features


<a id="org132b012"></a>

## Euler-Maruyama (EM) scheme

1.  Baseline model for comparisons,
2.  Numpy accelerated version,
3.  Numbas accelerated version,


<a id="org96fbb8e"></a>

## Function Benchmarking

1.  Performance timing for EM models,
2.  Time complexity across sampling and chains shown on clear 3d pyplot,


<a id="orge14c460"></a>

## Accuracy Analysis

1.  Exact solution calculated for efficiency estimates,
2.  Errors quantified and visualised,


<a id="orga2e71ae"></a>

## Runge-Kutta (RK) scheme

1.  Highly efficient RK scheme implemented in numpy,
2.  Strong and weak convergence for path-dependent options,


<a id="org76c50a0"></a>

## Exotic option pricing

1.  Use of numpy accelerated Monte Carlo sampling of RK scheme to price Bermudan shout option,
2.  **Antithetic sampling** for higher efficiency,
3.  Visualisation of paths and convergence,


<a id="org899e8d3"></a>

## Unit Testing and Input Validation

1.  Use of pytest to ensure edge cases considered,
2.  Input validation function for function safety.


<a id="org63d1757"></a>

# Installation

If you have git and pip,

    # download project
    git clone https://github.com/ghost9639/MATH5350-Assessment-2
    cd MATH5350-Assessment-2
    
    # install any required dependencies
    pip install numpy numba matplotlib pytest
    
    # alternatively, if you have nix
    nix-shell


<a id="orgc03fc9c"></a>

# Project Insights

1.  Numpy acceleration and Numba JIT compilation for high efficiency compared to base Python,
2.  Euler-Maruyama is easily debugged but lacks weak convergence for path independent options,
3.  Runge-Kutta scheme has higher computational cost but weak convergence,
4.  Antithetic sampling for faster convergence,


<a id="orgaf401f8"></a>

# Potential Improvements

1.  GPU acceleration,
2.  Further MC methods,
3.  Support for general and multi-dimensional SDEs,
4.  Calibration for real data.

