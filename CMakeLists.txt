project(pygobject C)
cmake_minimum_required(VERSION 2.8)
  
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set(PYGOBJECT_MAJOR_VERSION 3)
set(PYGOBJECT_MINOR_VERSION 3)
set(PYGOBJECT_MICRO_VERSION 3)
set(PYGOBJECT_VERSION "${PYGOBJECT_MAJOR_VERSION}.${PYGOBJECT_MINOR_VERSION}.${PYGOBJECT_MICRO_VERSION}")

set(PACKAGE "pygobject")
set(PACKAGE_BUGREPORT "http://bugzilla.gnome.org/enter_bug.cgi?product=pygobject")
set(PACKAGE_NAME "pygobject")
set(PACKAGE_URL "")
set(PACKAGE_VERSION ${PYGOBJECT_VERSION})
set(PACKAGE_STRING "${PACKAGE_NAME} ${PACKAGE_VERSION}")
set(PACKAGE_TARNAME "${PACKAGE_NAME}")

message(STATUS "Building ${PACKAGE_STRING}")

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config.h)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
add_definitions(-DHAVE_CONFIG_H)

#depdendencies
find_package(GLIB REQUIRED)
find_package(FFI REQUIRED)
find_package(GI REQUIRED)
			       
# Find Python executable  
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)

if(NOT PYTHONLIBS_FOUND OR NOT PYTHON_EXECUTABLE)
  message(SEND_ERROR "You need Python to build the dbus python bindings")
endif(NOT PYTHONLIBS_FOUND OR NOT PYTHON_EXECUTABLE)

# The code below prints the Python extension for the current system
set(get_python_suffix "import imp ; print(list(filter(lambda s : s[1] == 'rb' and s[0][0] == '.', imp.get_suffixes()))[0][0])")

execute_process(
  COMMAND ${PYTHON_EXECUTABLE} -c "${get_python_suffix}"
  OUTPUT_VARIABLE _modsuffix
)
string(REPLACE "\n" "" _modsuffix ${_modsuffix}) 
message(STATUS "Python module suffix is: ${_modsuffix}")

# The code below returns the site-packages directory for the current system
set(get_site_package_dir "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
execute_process(
  COMMAND ${PYTHON_EXECUTABLE} -c "${get_site_package_dir}"
  OUTPUT_VARIABLE site_pkg
)
string(REPLACE "\n" "" site_pkg ${site_pkg}) 
message(STATUS "Python module path is: ${site_pkg}")
message(STATUS "Python module suffix is: ${}")


get_filename_component(PYTHON_BASENAME "${PYTHON_EXECUTABLE}" NAME_WE)

include(_glib.cmake)
include(_gobject.cmake)
include(_gi.cmake)
