from launch import LaunchDescription

from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    hunav_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('hunav_gazebo_wrapper'),
                'launch',
                'small_house.launch.py'
            )
        )
    )

    human_markers_node = Node(
        package='agorabot_social_layer',
        executable='human_markers_node',
        name='human_markers_node',
        output='screen'
    )

    social_costmap_node = Node(
        package='agorabot_social_layer',
        executable='social_costmap_node',
        name='social_costmap_node',
        output='screen'
    )

    return LaunchDescription([
        hunav_launch,
        human_markers_node,
        social_costmap_node
    ])