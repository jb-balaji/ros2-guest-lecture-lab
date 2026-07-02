#!/usr/bin/env bash
# One-shot bootstrap for the lab workspace on Ubuntu 24.04 + ROS 2 Jazzy.
# Run from the repo root:  ./scripts/bootstrap.sh
set -euo pipefail

ROS_DISTRO="${ROS_DISTRO:-jazzy}"

echo "==> Installing apt dependencies for ROS 2 $ROS_DISTRO ..."
sudo apt update
sudo apt install -y \
    "ros-${ROS_DISTRO}-desktop" \
    "ros-${ROS_DISTRO}-nav2-bringup" \
    "ros-${ROS_DISTRO}-nav2-simple-commander" \
    "ros-${ROS_DISTRO}-turtlebot3" \
    "ros-${ROS_DISTRO}-turtlebot3-msgs" \
    "ros-${ROS_DISTRO}-turtlebot3-gazebo" \
    "ros-${ROS_DISTRO}-turtlebot3-cartographer" \
    "ros-${ROS_DISTRO}-turtlebot3-navigation2" \
    "ros-${ROS_DISTRO}-turtlebot3-teleop" \
    python3-colcon-common-extensions \
    python3-rosdep

echo "==> Initializing rosdep (safe to re-run) ..."
sudo rosdep init || true
rosdep update

echo "==> Resolving package-level dependencies ..."
( cd ros2_ws && rosdep install --from-paths src --ignore-src -r -y --rosdistro "$ROS_DISTRO" )

echo "==> Building the workspace ..."
(
  cd ros2_ws
  source "/opt/ros/${ROS_DISTRO}/setup.bash"
  colcon build --symlink-install
)

echo "==> Done. Add these lines to your shell rc (~/.bashrc):"
cat <<EOF

    source /opt/ros/${ROS_DISTRO}/setup.bash
    source $(pwd)/ros2_ws/install/setup.bash
    export TURTLEBOT3_MODEL=burger
    export GZ_SIM_RESOURCE_PATH=/opt/ros/${ROS_DISTRO}/share/turtlebot3_gazebo/models:\${GZ_SIM_RESOURCE_PATH}

EOF
