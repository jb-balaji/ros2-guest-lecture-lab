"""SLAM via TurtleBot3's native cartographer launch (with sim time on).

Thin wrapper around `turtlebot3_cartographer/cartographer.launch.py` so students
type one consistent `ros2 launch lab slam.launch.py` regardless of which
underlying stack we use.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    tb3_cartographer_share = get_package_share_directory('turtlebot3_cartographer')

    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='Use Gazebo clock.'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_cartographer_share, 'launch', 'cartographer.launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])
