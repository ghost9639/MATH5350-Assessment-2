// #include "MCSampling.hpp"
#include "App.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

py::array_t<double> InvNormWrapper (double, double, std::vector<size_t>);

PYBIND11_MODULE(MonteCarloSampling, m) {
  m.doc() = "Collection of Monte Carlo Sampling Methods";

  m.def("BoxMuller", &box_muller,
		"A Normal Distribution sampler based on the Box-Muller transform.");

  m.def("InverseNormalSampler", &InvNormWrapper,
		py::arg("mu") = 0.0,
		py::arg("sigma") = 1.0,
		py::arg("size") = std::vector<size_t>{1}),
  ("A Normal Distribution sampler based on the inverse quantile transform technique. Expects mu, sigma, and a size as a list.");
}

py::array_t<double> InvNormWrapper (double mu = 0.0, double sigma = 1.0, std::vector<size_t> shape = {1}) {

  ssize_t chain_len = 1;
  for (auto s : shape) { chain_len *= s; }

  auto data = ITNormalSampler (mu, sigma, shape);

  auto arr = py::array_t<double>(shape);
  std::memcpy(arr.mutable_data(), data.data(), chain_len * sizeof(double));

  return arr;
}
