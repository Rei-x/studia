cmake_minimum_required(VERSION 3.5)
project(TEP VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
set (CMAKE_CXX_STANDARD 98)
enable_testing()

file(GLOB files_to_test "${CMAKE_CURRENT_SOURCE_DIR}/laby*/*.test.cpp")

include_directories(${PROJECT_SOURCE_DIR})
if(BUILD_TESTING)
  foreach(filename ${files_to_test})
      string(REGEX MATCH "laby[0-9]+" laby ${filename})
      get_filename_component(filename_without_ext ${filename} NAME_WE)
      file(GLOB all_files
     "${CMAKE_CURRENT_SOURCE_DIR}/${laby}/*.h"
     "${CMAKE_CURRENT_SOURCE_DIR}/${laby}/*.cpp")
      set(exercise_name ${laby}-${filename_without_ext})
      add_executable(exercise_name ${all_files})
      add_test(NAME ${laby}/${filename_without_ext} COMMAND exercise_name)
  endforeach()
endif()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
