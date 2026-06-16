from launch import LaunchDescription

from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    #
    # Scenario argument
    #

    scenario_arg = DeclareLaunchArgument(
        "scenario",
        default_value="agents_house.yaml",
        description="HuNav scenario YAML file",
    )

    scenario = LaunchConfiguration("scenario")

    #
    # Gazebo GUI argument
    #

    launch_gazebo_gui_arg = DeclareLaunchArgument(
        "launch_gazebo_gui",
        default_value="True",
        description="Launch Gazebo GUI client (True/False). Set to False to reduce CPU/GPU load.",
    )

    launch_gazebo_gui = LaunchConfiguration("launch_gazebo_gui")

    #
    # HuNav launch
    #

    hunav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("hunav_gazebo_wrapper"),
                "launch",
                "small_house.launch.py",
            )
        ),
        launch_arguments={
            "configuration_file": scenario,
            "launch_gazebo_gui": launch_gazebo_gui,
        }.items(),
    )

    #
    # Human markers node
    #

    human_markers_node = Node(
        package="agorabot_social_layer",
        executable="human_markers_node",
        name="human_markers_node",
        output="screen",
    )

    #
    # Social costmap node
    #

    # social_costmap_node = Node(
    #     package="agorabot_social_layer",
    #     executable="social_costmap_node",
    #     name="social_costmap_node",
    #     output="screen",
    # )

    #
    # Social behavior node
    #

    social_behavior_node = Node(
        package="agorabot_social_layer",
        executable="social_behavior_node",
        name="social_behavior_node",
        output="screen",
    )

    #
    # Keepout filter mask server
    #

    # keepout_filter_mask_server = Node(
    #     package="nav2_map_server",
    #     executable="map_server",
    #     name="keepout_filter_mask_server",
    #     output="screen",
    #     parameters=[
    #         {
    #             "yaml_filename": os.path.join(
    #                 get_package_share_directory("agorabot_bringup"),
    #                 "maps",
    #                 "social_keepout_mask.yaml",
    #             ),
    #             "topic_name": "/keepout_filter_mask",
    #             "frame_id": "map",
    #         }
    #     ],
    # )

    #
    # Costmap filter info server
    #

    # costmap_filter_info_server = Node(
    #     package="nav2_map_server",
    #     executable="costmap_filter_info_server",
    #     name="costmap_filter_info_server",
    #     output="screen",
    #     parameters=[
    #         {
    #             "type": 0,
    #             "filter_info_topic": "/costmap_filter_info",
    #             "mask_topic": "/keepout_filter_mask",
    #             "base": 0.0,
    #             "multiplier": 1.0,
    #         }
    #     ],
    # )

    #
    # Lifecycle manager
    #

    # lifecycle_manager_filters = Node(
    #     package="nav2_lifecycle_manager",
    #     executable="lifecycle_manager",
    #     name="lifecycle_manager_costmap_filters",
    #     output="screen",
    #     parameters=[
    #         {
    #             "use_sim_time": True,
    #             "autostart": True,
    #             "node_names": [
    #                 "keepout_filter_mask_server",
    #                 "costmap_filter_info_server",
    #             ],
    #         }
    #     ],
    # )

    #
    # Launch everything
    #

    return LaunchDescription(
        [
            scenario_arg,
            launch_gazebo_gui_arg,
            hunav_launch,
            human_markers_node,
            # social_costmap_node,
            social_behavior_node,
            # keepout_filter_mask_server,
            # costmap_filter_info_server,
            # lifecycle_manager_filters,
        ]
    )
