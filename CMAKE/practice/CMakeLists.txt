cmake_minimum_required(VERSION 3.22.1)

project(game)

include_directories(include sub/include)
add_library(math STATIC lib/sub.cpp) 
set_target_properties(math PROPERTIES LINKER_LANGUAGE CXX)


add_executable(game src/main.cpp src/add.cpp)
target_link_libraries(game math subtraction)
add_subdirectory(sub)

