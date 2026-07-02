"""Launch TurtleBot3 in a Gazebo world 

Wraps the upstream `turtlebot3_gazebo` empty_world launch. Set the
TURTLEBOT3_MODEL environment variable to `burger`, `waffle`, or `waffle_pi`
before launching.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    world = LaunchConfiguration('world')
    model = LaunchConfiguration('model')

    tb3_gazebo_share = get_package_share_directory('turtlebot3_gazebo')
    tb3_models_dir = os.path.join(tb3_gazebo_share, 'models')
    existing_resource_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    resource_path = (
        f'{tb3_models_dir}:{existing_resource_path}' if existing_resource_path else tb3_models_dir
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='turtlebot3_world.launch.py',
            description='TurtleBot3 gazebo launch file to include '
                        '(turtlebot3_world.launch.py, turtlebot3_house.launch.py, empty_world.launch.py).',
        ),
        DeclareLaunchArgument(
            'model',
            default_value=os.environ.get('TURTLEBOT3_MODEL', 'burger'),
            description='TurtleBot3 model: burger | waffle | waffle_pi',
        ),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', model),
        # Ensure Gazebo can resolve `model://turtlebot3_world` (and friends)
        # referenced inside the .world files by adding the turtlebot3_gazebo
        # models directory to the resource search path.
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', resource_path),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3_gazebo_share, 'launch', 'turtlebot3_world.launch.py')
            ),
        ),
    ])
