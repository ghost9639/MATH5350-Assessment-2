# Project dependencies included in shell.nix
cmake_minimum_required(VERSION 3.5.0)
project(MonteCarloSampling LANGUAGES CXX)


# Cmake standard requirements
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_BUILD_TYPE Release)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON) # cmake ide flags



# =============================
# Google test
# =============================


include(CTest)

configure_file(CMakeLists.txt.in
        googletest-download/CMakeLists.txt)

execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )
execute_process(COMMAND ${CMAKE_COMMAND} --build .
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/googletest-download )


add_subdirectory(${CMAKE_BINARY_DIR}/googletest-src
        ${CMAKE_BINARY_DIR}/googletest-build)

# add_subdirectory(CPPTests)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

enable_testing()
add_subdirectory(CPPTests)



# =============================
# CPP app compilation
# =============================

# compiler warning flags
add_library(project_warnings INTERFACE)

target_compile_options(project_warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
)


add_library(MCCore STATIC
  src/App.cpp
)

target_include_directories(MCCore PUBLIC include)
target_include_directories(MCCore
  PUBLIC
      ${PROJECT_SOURCE_DIR}/include
)

add_executable(App
  src/main.cpp
)

target_link_libraries(App
  PRIVATE
  MCCore
  project_warnings
)

# # =============================
# # pybind
# # =============================
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG QUIET)

if (NOT pybind11_FOUND)
   include(FetchContent)
   message(STATUS "Couldn't find pybind, fetching from Git")
   FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG v2.12.0
   )
   FetchContent_MakeAvailable(pybind11)
endif()

pybind11_add_module(MonteCarloSampling pybind11/MonteCarloSampling.cpp)
target_link_libraries(MonteCarloSampling PRIVATE MCCore)
install (TARGETS MonteCarloSampling DESTINATION .)

