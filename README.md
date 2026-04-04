
# Table of Contents

1.  [Stochastic Differential Equation (SDE) Solver](#org44746ff)
2.  [Features](#org0a67cd2)
    1.  [Euler-Maruyama (EM) scheme](#orgca108ea)
    2.  [Function Benchmarking](#orgcc2a5e2)
    3.  [Accuracy Analysis](#org2b19dde)
    4.  [Runge-Kutta (RK) scheme](#orgd0cdecc)
    5.  [Exotic option pricing](#org1d6d851)
    6.  [Unit Testing and Input Validation](#org134d000)
3.  [Installation](#orgd09e4e3)
4.  [Project Insights](#orgb385fea)
5.  [Potential Improvements](#org6ceb4ba)



<a id="org44746ff"></a>

# Stochastic Differential Equation (SDE) Solver

This project implements a high performance SDE solver. It employs number of approaches towards solving a defined Stochastic Differential Equation modelling a stock price, and later Monte Carlo methods for estimating the price of a Bermudan shout option on the stock. Numpy and Numbas are used for optimal memory and runtime efficiency within Python.

$$d S_t = S_t \mu dt + S_t \sigma [1 + 0.9 \sin (2 \pi t)] d W_t$$

A seasonal volatility model is solved in the [full report](Report.pdf).


<a id="org0a67cd2"></a>

# Features


<a id="orgca108ea"></a>

## Euler-Maruyama (EM) scheme

1.  Baseline model for comparisons,
2.  Numpy accelerated version,
3.  Numbas accelerated version,


<a id="orgcc2a5e2"></a>

## Function Benchmarking

1.  Performance timing for EM models,
2.  Time complexity across sampling and chains shown on clear 3d pyplot,


<a id="org2b19dde"></a>

## Accuracy Analysis

1.  Exact solution calculated for efficiency estimates,
2.  Errors quantified and visualised,


<a id="orgd0cdecc"></a>

## Runge-Kutta (RK) scheme

1.  Highly efficient RK scheme implemented in numpy,
2.  Strong and weak convergence for path-dependent options,


<a id="org1d6d851"></a>

## Exotic option pricing

1.  Use of numpy accelerated Monte Carlo sampling of RK scheme to price Bermudan shout option,
2.  **Antithetic sampling** for higher efficiency,
3.  Visualisation of paths and convergence,


<a id="org134d000"></a>

## Unit Testing and Input Validation

1.  Use of pytest to ensure edge cases considered,
2.  Input validation function for function safety.


<a id="orgd09e4e3"></a>

# Installation

If you have git and pip,

    # download project
    git clone https://github.com/ghost9639/MATH5350-Assessment-2
    cd MATH5350-Assessment-2
    
    # install any required dependencies
    pip install numpy numba matplotlib
    
    # alternatively, if you have nix
    nix-shell


<a id="orgb385fea"></a>

# Project Insights

1.  Numpy acceleration and Numba JIT compilation for high efficiency compared to base Python,
2.  Euler-Maruyama is easily debugged but lacks weak convergence for path independent options,
3.  Runge-Kutta scheme has higher computational cost but weak convergence,
4.  Antithetic sampling for faster convergence,


<a id="org6ceb4ba"></a>

# Potential Improvements

1.  GPU acceleration,
2.  Further MC methods,
3.  Support for general and multi-dimensional SDEs,
4.  Calibration for real data.

