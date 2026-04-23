
# Table of Contents

1.  [Stochastic Differential Equation (SDE) Solver](#orgf746868)
2.  [C++ Integration](#orgf8250d6)
    1.  [Monte Carlo Sampling Library](#orgc89328b)
    2.  [Unit Testing](#org31f9957)
3.  [Features](#orgeb81baa)
    1.  [Euler-Maruyama (EM) scheme](#org73b2f3c)
    2.  [Function Benchmarking](#orgd4e856e)
    3.  [Accuracy Analysis](#org9a6947a)
    4.  [Runge-Kutta (RK) scheme](#orgd318ab0)
    5.  [Exotic option pricing](#org6026759)
    6.  [Unit Testing and Input Validation](#org2900799)
4.  [Installation](#org6c79285)
    1.  [Building Local Library](#org37ed8c9)
5.  [Project Insights](#orgeb7983d)
6.  [Potential Improvements](#orgc94e577)



<a id="orgf746868"></a>

# Stochastic Differential Equation (SDE) Solver

This project implements a high performance SDE solver. It employs number of approaches towards solving a defined Stochastic Differential Equation modelling a stock price, and later Monte Carlo methods for estimating the price of a Bermudan shout option on the stock. Numpy and Numbas are used for optimal memory and runtime efficiency within Python.

$$d S_t = S_t \mu dt + S_t \sigma [1 + 0.9 \sin (2 \pi t)] d W_t$$

A seasonal volatility model is solved in the [full report](Report.pdf). The [main file](Main.py) and [unit testing](testing.py) files are also available.


<a id="orgf8250d6"></a>

# C++ Integration


<a id="orgc89328b"></a>

## Monte Carlo Sampling Library

This project features a Main Monte Carlo engine written entirely in C++, which connects to Python using [pybind11](https://github.com/pybind/pybind11). The high speed library includes an inverse quantile transform leveraging Padé approximation based on Abramowitz and Stegun. Documentation is included [for library functions](docs/html/index.html). All functions export to vectorised numpy arrays, which work extremely well with pandas and numpy functions in general. This ensures seamless integration into existing toolsets.


<a id="org31f9957"></a>

## Unit Testing

This project uses [Google Test](https://github.com/google/googletest) to validate internal function accuracy, ensuring that the logic remains reliable under changes. Tests can be accessed by using the typical CTest commands (\`cmake &ndash;build build &ndash;target test\`).


<a id="orgeb81baa"></a>

# Features


<a id="org73b2f3c"></a>

## Euler-Maruyama (EM) scheme

1.  Baseline model for comparisons,
2.  Numpy accelerated version,
3.  Numbas accelerated version,


<a id="orgd4e856e"></a>

## Function Benchmarking

1.  Performance timing for EM models,
2.  Time complexity across sampling and chains shown on clear 3d pyplot,


<a id="org9a6947a"></a>

## Accuracy Analysis

1.  Exact solution calculated for efficiency estimates,
2.  Errors quantified and visualised,


<a id="orgd318ab0"></a>

## Runge-Kutta (RK) scheme

1.  Highly efficient RK scheme implemented in numpy,
2.  Strong and weak convergence for path-dependent options,


<a id="org6026759"></a>

## Exotic option pricing

1.  Use of numpy accelerated Monte Carlo sampling of RK scheme to price Bermudan shout option,
2.  **Antithetic sampling** for higher efficiency,
3.  Visualisation of paths and convergence,


<a id="org2900799"></a>

## Unit Testing and Input Validation

1.  Use of pytest to ensure edge cases considered,
2.  Input validation function for function safety.


<a id="org6c79285"></a>

# Installation

If you have git and pip,

    # download project
    git clone https://github.com/ghost9639/MATH5350-Assessment-2
    cd MATH5350-Assessment-2
    
    # install any required dependencies
    pip install numpy numba matplotlib pytest
    
    # alternatively, if you have nix
    nix-shell


<a id="org37ed8c9"></a>

## Building Local Library

Building the local library is easy and requires relatively few build tools, depending on a C++17 installation, CMake (any version above 3.5), Git, and Ninja. On MacOS / Linux:

    git clone https://github.com/ghost9639/Monte-Carlo-Engine
    cd Monte-Carlo-Engine
    
    rm -rf build
    mkdir build
    
    cmake -S . -B build -G Ninja
    cmake --build build
    
    export PYTHONPATH=$PYTHONPATH:$(pwd)/build
    python <YOUR_PYTHON_FILE>

On Windows:

    git clone https://github.com/ghost9639/Monte-Carlo-Engine
    cd Monte-Carlo-Engine
    
    cmake -S . -B build -G Ninja
    cmake --build build
    
    # One of:
    set PYTHONPATH=%PYTHONPATH%;%cd%\build # if using cmd
    $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)\build" # if using powershell
    
    python <YOUR_PYTHON_FILE>


<a id="orgeb7983d"></a>

# Project Insights

1.  Numpy acceleration and Numba JIT compilation for high efficiency compared to base Python,
2.  Euler-Maruyama is easily debugged but lacks weak convergence for path independent options,
3.  Runge-Kutta scheme has higher computational cost but weak convergence,
4.  Antithetic sampling for faster convergence,


<a id="orgc94e577"></a>

# Potential Improvements

1.  GPU acceleration,
2.  Further MC methods,
3.  Support for general and multi-dimensional SDEs,
4.  Calibration for real data.

