#pragma once

#include <string>
#include <unordered_map>

class distribution {
public:
  std::string name;				// whatever the distribution is called 
  std::unordered_map <std::string, double> moments; // moments that characterise it

//   virtual double get_quantile(std::unordered_map <std::string, double>, );
  virtual double get_percentile();
//   virtual double 

};
