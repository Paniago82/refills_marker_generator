execute_process(COMMAND "/home/john/ubica_ws/src/refills_marker_generator/cmake-build-debug/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/john/ubica_ws/src/refills_marker_generator/cmake-build-debug/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
