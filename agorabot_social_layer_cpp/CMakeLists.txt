cmake_minimum_required(VERSION 3.8)
project(agorabot_social_layer_cpp)

find_package(ament_cmake REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(pluginlib REQUIRED)
find_package(hunav_msgs REQUIRED)

include_directories(include)

add_library(social_layer SHARED
  src/social_layer.cpp
)

ament_target_dependencies(social_layer
  nav2_costmap_2d
  pluginlib
  hunav_msgs
)

pluginlib_export_plugin_description_file(
  nav2_costmap_2d
  social_layer_plugin.xml
)

install(
  TARGETS social_layer
  DESTINATION lib
)

install(
  DIRECTORY include/
  DESTINATION include/
)

install(
  FILES social_layer_plugin.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()