
# Table of Contents

1.  [Stochastic Differential Equation (SDE) Solver](#org7f54ae6)
2.  [C++ Integration](#org3628d71)
    1.  [Monte Carlo Sampling Library](#org35f8760)
    2.  [Unit Testing](#org45c0f99)
    3.  [Building Local Library](#org66a866e)
3.  [Features](#orgd68b613)
    1.  [Euler-Maruyama (EM) scheme](#org33c0d2e)
    2.  [Function Benchmarking](#org60d6b3d)
    3.  [Accuracy Analysis](#org48d4339)
    4.  [Runge-Kutta (RK) scheme](#org36f1a3c)
    5.  [Exotic option pricing](#orgfd64005)
    6.  [Unit Testing and Input Validation](#org3c5ada8)
4.  [Installation](#orgd0cc18d)
5.  [Project Insights](#org9800906)
6.  [Potential Improvements](#org166910f)



<a id="org7f54ae6"></a>

# Stochastic Differential Equation (SDE) Solver

This project implements a high performance SDE solver. It employs number of approaches towards solving a defined Stochastic Differential Equation modelling a stock price, and later Monte Carlo methods for estimating the price of a Bermudan shout option on the stock. Numpy and Numbas are used for optimal memory and runtime efficiency within Python.

$$d S_t = S_t \mu dt + S_t \sigma [1 + 0.9 \sin (2 \pi t)] d W_t$$

A seasonal volatility model is solved in the [full report](Report.pdf). The [main file](Main.py) and [unit testing](testing.py) files are also available.


<a id="org3628d71"></a>

# C++ Integration


<a id="org35f8760"></a>

## Monte Carlo Sampling Library

This project features a Main Monte Carlo engine written entirely in C++, which connects to Python using [pybind11](https://github.com/pybind/pybind11). The high speed library includes an inverse quantile transform leveraging Padé approximation based on Abramowitz and Stegun. Documentation is included [for library functions](docs/html/index.html). All functions export to vectorised numpy arrays, which work extremely well with pandas and numpy functions in general. This ensures seamless integration into existing toolsets.


<a id="org45c0f99"></a>

## Unit Testing

This project uses [Google Test](https://github.com/google/googletest) to validate internal function accuracy, ensuring that the logic remains reliable under changes. Tests can be accessed by using the typical CTest commands (\`cmake &ndash;build build &ndash;target test\`).


<a id="org66a866e"></a>

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


<a id="orgd68b613"></a>

# Features


<a id="org33c0d2e"></a>

## Euler-Maruyama (EM) scheme

1.  Baseline model for comparisons,
2.  Numpy accelerated version,
3.  Numbas accelerated version,


<a id="org60d6b3d"></a>

## Function Benchmarking

1.  Performance timing for EM models,
2.  Time complexity across sampling and chains shown on clear 3d pyplot,


<a id="org48d4339"></a>

## Accuracy Analysis

1.  Exact solution calculated for efficiency estimates,
2.  Errors quantified and visualised,


<a id="org36f1a3c"></a>

## Runge-Kutta (RK) scheme

1.  Highly efficient RK scheme implemented in numpy,
2.  Strong and weak convergence for path-dependent options,


<a id="orgfd64005"></a>

## Exotic option pricing

1.  Use of numpy accelerated Monte Carlo sampling of RK scheme to price Bermudan shout option,
2.  **Antithetic sampling** for higher efficiency,
3.  Visualisation of paths and convergence,


<a id="org3c5ada8"></a>

## Unit Testing and Input Validation

1.  Use of pytest to ensure edge cases considered,
2.  Input validation function for function safety.


<a id="orgd0cc18d"></a>

# Installation

If you have git and pip,

    # download project
    git clone https://github.com/ghost9639/MATH5350-Assessment-2
    cd MATH5350-Assessment-2
    
    # install any required dependencies
    pip install numpy numba matplotlib pytest
    
    # alternatively, if you have nix
    nix-shell


<a id="org9800906"></a>

# Project Insights

1.  Numpy acceleration and Numba JIT compilation for high efficiency compared to base Python,
2.  Euler-Maruyama is easily debugged but lacks weak convergence for path independent options,
3.  Runge-Kutta scheme has higher computational cost but weak convergence,
4.  Antithetic sampling for faster convergence,


<a id="org166910f"></a>

# Potential Improvements

1.  GPU acceleration,
2.  Further MC methods,
3.  Support for general and multi-dimensional SDEs,
4.  Calibration for real data.

