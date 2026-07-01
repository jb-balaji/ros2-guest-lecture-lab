#!/usr/bin/env python3
"""Send a list of waypoints to Nav2 using nav2_simple_commander.

Edit the WAYPOINTS list below to change where the robot goes.
Coordinates are in the `map` frame; you can read them off RViz by hovering.
"""

import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


# (x, y, yaw_radians) in the map frame. Edit me!
WAYPOINTS = [
    (1.5,  0.5,  0.0),
    (1.5, -0.5, -math.pi / 2),
    (-1.5, -0.5,  math.pi),
    (-1.5,  0.5,  math.pi / 2),
]

# Initial pose of the robot (where AMCL should start guessing).
# Match this to the robot's spawn pose in the launched Gazebo world.
INITIAL_POSE = (0.0, 0.0, 0.0)


def make_pose(navigator: BasicNavigator, x: float, y: float, yaw: float) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main() -> None:
    rclpy.init()
    navigator = BasicNavigator()

    initial = make_pose(navigator, *INITIAL_POSE)
    navigator.setInitialPose(initial)

    navigator.waitUntilNav2Active()

    goals = [make_pose(navigator, *wp) for wp in WAYPOINTS]
    navigator.followWaypoints(goals)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback is not None:
            navigator.get_logger().info(
                f'On waypoint {feedback.current_waypoint + 1} / {len(goals)}'
            )

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info('All waypoints reached.')
    elif result == TaskResult.CANCELED:
        navigator.get_logger().warn('Waypoint following was canceled.')
    elif result == TaskResult.FAILED:
        navigator.get_logger().error('Waypoint following failed.')

    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
