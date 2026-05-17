cmake_minimum_required(VERSION 3.8)
project(agorabot_bt_nodes)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)

add_library(is_social_wait_condition_bt_node SHARED
  src/is_social_wait_condition.cpp
)

target_compile_definitions(is_social_wait_condition_bt_node PRIVATE BT_PLUGIN_EXPORT)

ament_target_dependencies(is_social_wait_condition_bt_node
  rclcpp
  std_msgs
  behaviortree_cpp_v3
)

install(TARGETS is_social_wait_condition_bt_node
  LIBRARY DESTINATION lib
)

ament_package()