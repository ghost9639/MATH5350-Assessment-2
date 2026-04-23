#include <iostream>
#include <vector>
#include "App.hpp"
#include <random>
#include <memory>

int main() { 

  // std::random_device rand; // single declaration single use
  // std::mt19937 eng(rand());
  // std::uniform_real_distribution<> distrib(0, 1);

  // // try out the box_muller
  // std::vector<double> bm_normal_samples = box_muller(eng, distrib);

  // std::cout<<"Our samples from the Box-Muller approach are:";
  
    
  // // why not just define a list of variables for now
  // std::unique_ptr<std::vector<double>> Thread1 = std::make_unique<std::vector<double>> ();

  // for (unsigned i = 0; i < 10; i++) {
  // 	Thread1 -> push_back(distrib(eng));
  // }

  // for (auto i : *Thread1) {
  // 	std::cout<<"Our random vector contains "<<i<<std::endl;
  // }

  std::vector<size_t> sh = {10000};
  auto normsamps = ITNormalSampler (1245, 2, sh);

  double moment_1 = 0.0;
  for (auto elem : normsamps) {
	moment_1 += elem;
  }

  moment_1 /= 10000;

  double moment_2 = 0.0;

  for (auto elem : normsamps) {
	moment_2 += (elem*elem);
  }

  moment_2 /= 10000;

  // looks good to me
  std::cout<< "The first moment is " << moment_1 << " and the variance is " << (moment_2 - moment_1*moment_1) <<std::endl;
  
  return 0;

}
