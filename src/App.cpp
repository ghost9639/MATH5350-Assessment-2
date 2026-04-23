/**
 * @file App.cpp
 *
 * @brief A description of the currently implemented methods in this project.
 */

#include <cmath>
#include <iostream>
#include <random>
#include <vector>
#include "App.hpp"
#include "function.hpp"
#include <stdexcept>


// easiest method would be the box_muller approach

// generates two random Z variables from uniform distribution over [0, 1], this errors due to
// obscure bug where arm64 compiler can mischaracterise floating point paired returns on older
// gcc versions, can make wrapper Double class to fix this
/**
 * This function implements the Box-Muller approach to sampling random normal variables. By visualising
 * the uniform distribution on [0,1] as the length of a unit circle, we can exploit the polar form of
 * the length to transform a uniform variable sample to two normal distribution samples
 *
 * @param mu The mu parameter of the normal distribution
 * @param sigma the standard deviation of the normal distribution
 * @return samples a vector of two doubles, both samples from the normal distribution
 */
std::vector<double> box_muller (double mu = 0.0, double sigma = 1.0) {  

  std::random_device rand;
  std::mt19937 eng(rand());
  std::uniform_real_distribution<> dist;

  double unif_1 = dist(eng);
  double unif_2 = dist(eng);

  std::vector<double> samples;
  
  samples.push_back((std::sqrt(-2 * std::log(unif_1)) * std::cos(2 * M_PI * unif_2)) * sigma + mu);
  samples.push_back((std::sqrt(-2 * std::log(unif_1)) * std::sin(2 * M_PI * unif_2)) * sigma + mu);
  
  return samples;
}


// But what about the inverse quantile transform? could that be faster if hard-coded?
// what are the floating point precision errors? - listed approximation is accurate to
// 4.5e-5 and base doubles are 64 bit shouldn't be relevant
// https://www.johndcook.com/normal_cdf_inverse.html

/**
 * This set of functions leverages the inverse quantile transform to sample from the normal distribution.
 * The STL provides implementations for random uniform draws on a continuous space, and we can leverage
 * the Abramowitz and Stegun Handbook of Mathematical Functions (26.2.3) Normal Distribution approximation
 * in order to accurately convert the samples.
 *
 * The blog of John D. Cook https://www.johndcook.com/normal_cdf_inverse.html was a major influence on this
 * implementation, as well as the A&S Handbook https://personal.math.ubc.ca/~cbm/aands/frameindex.htm
 */

/**
 * This function directly calculates the Abramowitz and Stegun Padé-style approximation. It expects a value
 * t, which can be converted from a probability draw on [0,1] as \sqrt{\frac{1}{t^2}}.
 *
 * @param t the transformed probability of observing the respective x
 * @return x a double, the respective normal draw for the transformed probability
 */
double AnSApproximation (double t) { 
  // 
  double c_arr[] = {2.515517, 0.802853, 0.010328};
  double d_arr[] = {1.432788, 0.189269, 0.001308};

  return t - (((c_arr[2] * t + c_arr[1]) * t + c_arr[0]) /
			  (((d_arr[2] * t + d_arr[1])*t + d_arr[0])*t + 1));
}

/**
 * NormalInverse cleans and feeds sampled probabilities into the AnSApproximation function. It expects
 * one double value on the interval [0,1], and returns the corresponding (approximated) normal distribution
 * value.
 *
 * @param UniformSample A double value over [0,1] sampled from a probability (uniform) distribution
 * @return x a double value, the corresponding sample for the given probability sample
 */
double NormalInverse (double UniformSample) {  

  // limiting to domain of function
  if (UniformSample < 0.0 || UniformSample > 1.0) {
	std::cout<<"Sampled value of " << UniformSample <<" is outside required bounds."<<std::endl;
	std::cout<<"Sample must be between 0 and 1.";
	throw std::domain_error ("Sample from uniform distribution");
  }

  // approximation does not hold for p > .5
  if (UniformSample < 0.5) {
	// \Phi(p) = -Q^-1(p) (symmetric distribution)
	return -AnSApproximation(std::sqrt(-2.0 * std::log(UniformSample)));

  } else {
	// \Phi(p) = Q^-1(1-p)
	return AnSApproximation(std::sqrt(-2.0 * std::log(1-UniformSample)));
  }
  
}

/**
 * This ITNormalSampler is the frontend function that takes in the parameters of the normal distribution
 * and the requested samples and returns a vector corresponding to the required shape in 1D. Wrapper function
 * cleans it up for Python.
 *
 * @param shape Same shape vector as numpy.random.normal, the function will create a 1D vector of samples
 * @param mu The first moment of the normal distribution, defaults to 0
 * @param sigma The root of the second moment of the normal distribution, defaults to 1
 * @return NormalSamples a vector of random normal variable samples
 */
std::vector<double> ITNormalSampler (double mu = 0.0, double sigma = 1.0, std::vector<size_t> shape = {1}) { 

  // randomness engine declared once for speed
  std::random_device rand;
  std::mt19937 eng(rand());
  std::uniform_real_distribution<> dist;

  // 1D vector of samples
  std::vector<double> NormalSamples;
  
  try{
	
	ssize_t chain_len = 1;
	for (auto s : shape) { chain_len *= s; }

	for (ssize_t i = 0; i < chain_len; i++) {
	  NormalSamples.push_back(NormalInverse(dist(eng)) * sigma + mu);
	}
	
  }
  catch (std::domain_error) {
	// why do this? I guess if the error is from this porcelain it's a deeper error than just a bad entry?
	throw std::runtime_error ("Internal function logic error or faulty uniform real distribution function used");
  }
  
  
  return NormalSamples;
}


// when are we extending the "function" functionality for the inverse transform? worth writing RDParser
// to take in user inputs?
