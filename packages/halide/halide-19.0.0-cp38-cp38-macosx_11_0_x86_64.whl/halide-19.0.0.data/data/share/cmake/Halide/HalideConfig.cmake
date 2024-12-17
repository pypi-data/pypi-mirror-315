cmake_minimum_required(VERSION 3.28)

include(CMakeFindDependencyMacro)
find_dependency(Python 3)

include("${Python_SITEARCH}/halide/lib/cmake/Halide/HalideConfig.cmake")
