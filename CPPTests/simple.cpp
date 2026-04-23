// #include "../include/App.hpp"
#include "App.hpp"
#include <gtest/gtest.h>

TEST(ExampleTest_Succeeds, TestsWhetherConnected){
  EXPECT_EQ(example_function(10), 11);
  EXPECT_NE(example_function(10), 12);
}



// int simple() {
//   return 0;
// }
