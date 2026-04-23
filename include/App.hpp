#pragma once
#include <random>

int example_function(int);

std::vector<double> box_muller (double, double);
double AnSApproximation(double);
double NormalInverse (double);
std::vector<double> ITNormalSampler (double, double, std::vector<size_t>);
