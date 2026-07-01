"""Nav2 via TurtleBot3's native navigation2 launch (with sim time on).

Thin wrapper around `turtlebot3_navigation2/navigation2.launch.py`. Defaults
the editable nav2 params file to our local copy so the bug-hunt stretch task
(crank `inflation_radius` and watch planning fail) works without touching
system files.

Usage:
    ros2 launch lab nav2.launch.py                       # uses TB3's default map
    ros2 launch lab nav2.launch.py map:=$HOME/my_map.yaml
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    tb3_nav_share = get_package_share_directory('turtlebot3_navigation2')
    lab_share = get_package_share_directory('lab')

    default_map = os.path.join(tb3_nav_share, 'map', 'map.yaml')
    default_params = os.path.join(lab_share, 'config', 'nav2_params.yaml')

    map_yaml = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=default_map,
                              description='Full path to map yaml.'),
        DeclareLaunchArgument('params_file', default_value=default_params,
                              description='Full path to Nav2 params yaml (editable lab copy).'),
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='Use Gazebo clock.'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_nav_share, 'launch', 'navigation2.launch.py')
            ),
            launch_arguments={
                'map': map_yaml,
                'params_file': params_file,
                'use_sim_time': use_sim_time,
            }.items(),
        ),
    ])
