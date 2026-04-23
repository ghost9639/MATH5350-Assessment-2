#pragma once
#include <string>

class Function {

private:
  std::string id;
  std::string inverse; 

public:
  Function (std::string id, std::string inverse) {
	this->id = id; this->inverse = inverse; 
  }
  
  std::string get_id() { return id; }
  std::string get_inverse() { return inverse; }
  double test_inv (double val) { return val + 2; }
  
};
