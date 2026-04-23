#include "App.hpp"
#include <gtest/gtest.h>
#include <stdexcept>

TEST(NormalInverse_BadEntry, TestsBoundsChecking) {
  EXPECT_THROW(NormalInverse(-1), std::domain_error);
  EXPECT_THROW(NormalInverse(1.3), std::domain_error);
}

TEST(Normalnverse_Accuracy, TestsAccuracy) {
  EXPECT_NEAR(NormalInverse(1e-07), -5.1993375821928165, 0.00045);
  EXPECT_NEAR(NormalInverse(1e-06), -4.753424308822899, 0.00045);
  EXPECT_NEAR(NormalInverse(0.0001), -3.7190164854556804, 0.00045);
  EXPECT_NEAR(NormalInverse(0.1), -1.2815515655446004, 0.00045);
  EXPECT_NEAR(NormalInverse(0.3), -0.5244005127080409, 0.00045);
  EXPECT_NEAR(NormalInverse(0.5), 0.0, 0.00045);
  EXPECT_NEAR(NormalInverse(0.6), 0.2533471031357997, 0.00045);
  EXPECT_NEAR(NormalInverse(0.744), 0.6557266787982534, 0.00045);
  EXPECT_NEAR(NormalInverse(0.819), 0.9115607350675405, 0.00045);
  EXPECT_NEAR(NormalInverse(0.956), 1.7060433968889614, 0.00045);
  EXPECT_NEAR(NormalInverse(0.99999), 4.264890793923841, 0.00045);
}
