# source directory to current directory
set(SRC_DIR ${CMAKE_CURRENT_LIST_DIR})

# catch all local project files
file(GLOB_RECURSE ${SRC_DIR}/*.cpp)
