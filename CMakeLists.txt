cmake_minimum_required(VERSION 3.5.0)
project(phantomjs)

set (CMAKE_CXX_STANDARD 11)

if(APPLE)
  # Help Homebrew users by hinting the common keg paths when no prefix was provided.
  foreach(_qt_hint IN ITEMS "/opt/homebrew/opt/qt@5" "/usr/local/opt/qt@5")
    if(EXISTS "${_qt_hint}" AND NOT _qt_hint STREQUAL "")
      list(APPEND CMAKE_PREFIX_PATH "${_qt_hint}")
    endif()
  endforeach()
  foreach(_qtwebkit_hint IN ITEMS "/opt/homebrew/opt/qtwebkit" "/usr/local/opt/qtwebkit")
    if(EXISTS "${_qtwebkit_hint}" AND NOT _qtwebkit_hint STREQUAL "")
      list(APPEND CMAKE_PREFIX_PATH "${_qtwebkit_hint}")
    endif()
  endforeach()
endif()

find_package(Qt5 COMPONENTS Core Network WebKitWidgets REQUIRED)
find_package(Threads REQUIRED)
find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)

message("Using Qt version ${Qt5Core_VERSION}")
if (Qt5Core_VERSION VERSION_LESS 5.12.0)
  message(FATAL_ERROR "This version of Qt is not supported. Please use Qt 5.12 or later")
endif()
if(NOT Python3_FOUND)
  message(FATAL_ERROR "Python 3.10+ is required to run 'make check'. Install python@3.14 and rerun CMake.")
endif()

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

file(GLOB_RECURSE PHANTOMJS_SOURCES src/*.cpp)
include_directories(src)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(THIRDPARTY_SOURCES src/mongoose/mongoose.c src/qcommandline/qcommandline.cpp src/linenoise/src/linenoise.c)
include_directories(src/linenoise/src)
include_directories(src/mongoose)
include_directories(src/qcommandline)

if (WIN32)
  set(EXTRA_LIBS ws2_32)
  add_definitions(-DQCOMMANDLINE_STATIC)
else()
  set(EXTRA_LIBS dl)
endif()

add_executable(${PROJECT_NAME} src/phantomjs.qrc ${PHANTOMJS_SOURCES} ${THIRDPARTY_SOURCES})
target_link_libraries(${PROJECT_NAME} ${EXTRA_LIBS} Qt5::Core Qt5::Network Qt5::WebKitWidgets Threads::Threads)
install(TARGETS ${PROJECT_NAME} DESTINATION bin)

add_custom_target(check COMMAND "${Python3_EXECUTABLE}" test/run-tests.py -v)
