cmake_minimum_required(VERSION 3.2)
project(photoeditor_cpp)

find_package( OpenCV REQUIRED )

file(GLOB_RECURSE LIB_SOURCES "src/lib/*.cpp")
add_library(photoeditor_cpp_lib SHARED ${LIB_SOURCES})
target_include_directories(photoeditor_cpp_lib PUBLIC src/include  ${OpenCV_INCLUDE_DIRS} )
target_link_libraries(photoeditor_cpp_lib PUBLIC ${OpenCV_LIBS} )

add_subdirectory(pybind11)
pybind11_add_module(photoeditor_cpp src/python.cpp)
target_compile_definitions(photoeditor_cpp
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
target_link_libraries(photoeditor_cpp PUBLIC photoeditor_cpp_lib)