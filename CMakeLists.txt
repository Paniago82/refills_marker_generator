cmake_minimum_required(VERSION 2.8.3)
project(refills_marker_generator)

find_package(catkin REQUIRED COMPONENTS rospy)

catkin_python_setup()

catkin_package()

catkin_install_python(PROGRAMS scripts/gen_chilitags DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})