include_directories("${PROJECT_SOURCE_DIR}")

# tests
add_executable(INTests
  InverseNormalTests.cpp
)

# built tests
target_link_libraries(INTests
    MCCore
    gtest_main
)

add_test(NAME InverseNormalTests COMMAND INTests)

