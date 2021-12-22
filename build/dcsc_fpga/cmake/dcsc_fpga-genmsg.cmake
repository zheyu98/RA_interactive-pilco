# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "dcsc_fpga: 2 messages, 3 services")

set(MSG_I_FLAGS "-Idcsc_fpga:/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(dcsc_fpga_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_custom_target(_dcsc_fpga_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dcsc_fpga" "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_custom_target(_dcsc_fpga_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dcsc_fpga" "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" ""
)

get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_custom_target(_dcsc_fpga_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dcsc_fpga" "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" "dcsc_fpga/MopsSensors:std_msgs/Header"
)

get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_custom_target(_dcsc_fpga_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dcsc_fpga" "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" "dcsc_fpga/MopsActuators"
)

get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_custom_target(_dcsc_fpga_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "dcsc_fpga" "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
)
_generate_msg_cpp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
)

### Generating Services
_generate_srv_cpp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_cpp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_cpp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
)

### Generating Module File
_generate_module_cpp(dcsc_fpga
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(dcsc_fpga_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(dcsc_fpga_generate_messages dcsc_fpga_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_cpp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_cpp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_cpp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_cpp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_cpp _dcsc_fpga_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dcsc_fpga_gencpp)
add_dependencies(dcsc_fpga_gencpp dcsc_fpga_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dcsc_fpga_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
)
_generate_msg_eus(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
)

### Generating Services
_generate_srv_eus(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_eus(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_eus(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
)

### Generating Module File
_generate_module_eus(dcsc_fpga
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(dcsc_fpga_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(dcsc_fpga_generate_messages dcsc_fpga_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_eus _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_eus _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_eus _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_eus _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_eus _dcsc_fpga_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dcsc_fpga_geneus)
add_dependencies(dcsc_fpga_geneus dcsc_fpga_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dcsc_fpga_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
)
_generate_msg_lisp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
)

### Generating Services
_generate_srv_lisp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_lisp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_lisp(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
)

### Generating Module File
_generate_module_lisp(dcsc_fpga
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(dcsc_fpga_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(dcsc_fpga_generate_messages dcsc_fpga_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_lisp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_lisp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_lisp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_lisp _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_lisp _dcsc_fpga_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dcsc_fpga_genlisp)
add_dependencies(dcsc_fpga_genlisp dcsc_fpga_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dcsc_fpga_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
)
_generate_msg_nodejs(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
)

### Generating Services
_generate_srv_nodejs(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_nodejs(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_nodejs(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
)

### Generating Module File
_generate_module_nodejs(dcsc_fpga
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(dcsc_fpga_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(dcsc_fpga_generate_messages dcsc_fpga_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_nodejs _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_nodejs _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_nodejs _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_nodejs _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_nodejs _dcsc_fpga_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dcsc_fpga_gennodejs)
add_dependencies(dcsc_fpga_gennodejs dcsc_fpga_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dcsc_fpga_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
)
_generate_msg_py(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
)

### Generating Services
_generate_srv_py(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_py(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv"
  "${MSG_I_FLAGS}"
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
)
_generate_srv_py(dcsc_fpga
  "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
)

### Generating Module File
_generate_module_py(dcsc_fpga
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(dcsc_fpga_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(dcsc_fpga_generate_messages dcsc_fpga_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsSensors.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_py _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/msg/MopsActuators.msg" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_py _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsRead.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_py _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/MopsWrite.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_py _dcsc_fpga_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/zheyu/Desktop/RA/real_pend/src/dcsc_fpga/srv/Contr.srv" NAME_WE)
add_dependencies(dcsc_fpga_generate_messages_py _dcsc_fpga_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(dcsc_fpga_genpy)
add_dependencies(dcsc_fpga_genpy dcsc_fpga_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS dcsc_fpga_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/dcsc_fpga
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(dcsc_fpga_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/dcsc_fpga
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(dcsc_fpga_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/dcsc_fpga
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(dcsc_fpga_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/dcsc_fpga
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(dcsc_fpga_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/dcsc_fpga
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(dcsc_fpga_generate_messages_py std_msgs_generate_messages_py)
endif()
