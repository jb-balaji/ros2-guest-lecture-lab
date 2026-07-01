# ROS 2 Guest Lecture — TurtleBot3 + Nav2 Lab

> Companion ROS 2 workspace for the 90-minute guest lecture *"ROS 2 and Autonomous Mobile Robots"*.
> Use it as a **The Construct ROSject** or as a **local Ubuntu 24.04 + ROS 2 Jazzy** install (instructor's Plan B laptop).

This repo contains exactly what students need for the three hands-on blocks:

1. **First contact** — list nodes/topics, teleop a TurtleBot3 in Gazebo.
2. **SLAM** — drive around, watch a map appear, save it.
3. **Nav2** — set a 2D goal, run a Python waypoint follower, break and fix the costmap.

---

## What's inside

```
ros2_ws/
└── src/
    └── lab/
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        ├── resource/lab
        ├── lab/
        │   ├── __init__.py
        │   └── waypoint_follower.py     # uses nav2_simple_commander
        ├── launch/
        │   ├── sim.launch.py            # wraps turtlebot3_gazebo/turtlebot3_world
        │   ├── slam.launch.py           # wraps turtlebot3_cartographer (use_sim_time=true)
        │   └── nav2.launch.py           # wraps turtlebot3_navigation2 (loads our editable params)
        ├── config/
        │   ├── nav2_params.yaml         # editable copy of TB3's burger.yaml, with bug-hunt comments
        │   └── waypoints.yaml           # default waypoint list (optional)
        ├── maps/
        │   └── README.md                # how to generate a backup map (or just use TB3's default)
        └── README.md                    # short student-facing pointer
```

All three launch files are **thin wrappers** around the upstream TurtleBot3 launches. We add `use_sim_time:=true` and a writable `nav2_params.yaml` so students can do the bug-hunt stretch task without touching system files. Everything else is native.

---

## Quick start — local Ubuntu 24.04 + ROS 2 ${ROS_DISTRO}

```bash
# 1. Install dependencies (one-time)
sudo apt update
sudo apt install -y \
    ros-${ROS_DISTRO}-desktop \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-nav2-simple-commander \
    ros-${ROS_DISTRO}-turtlebot3 \
    ros-${ROS_DISTRO}-turtlebot3-gazebo \
    ros-${ROS_DISTRO}-turtlebot3-cartographer \
    ros-${ROS_DISTRO}-turtlebot3-navigation2 \
    ros-${ROS_DISTRO}-turtlebot3-teleop \
    python3-colcon-common-extensions

# 2. Build
cd ros2_ws
colcon build --symlink-install
source install/setup.bash

# 3. Set the robot model (required by TurtleBot3 packages every shell)
export TURTLEBOT3_MODEL=waffle
# Add to ~/.bashrc to persist:
echo 'export TURTLEBOT3_MODEL=waffle' >> ~/.bashrc

# 4. Run — three terminals, in this order
# Terminal A: Gazebo + TurtleBot3
ros2 launch lab sim.launch.py

# Terminal B (Hands-on 1): teleop
ros2 run turtlebot3_teleop teleop_keyboard

# Terminal B (Hands-on 2): SLAM (stop teleop first or keep both)
ros2 launch lab slam.launch.py
# When the map looks good, save it:
ros2 run nav2_map_server map_saver_cli -f ~/my_map

# Terminal B (Hands-on 3): Nav2 with your map
ros2 launch lab nav2.launch.py map:=$HOME/my_map.yaml
# In another terminal, run the waypoint follower:
ros2 run lab waypoint_follower
```

---

## Quick start — The Construct ROSject

1. Create a free account at https://app.theconstruct.ai/signup/.
2. Create a new ROSject based on the **ROS 2 Jazzy + Gazebo** template (or Humble if Jazzy isn't offered).
3. In the ROSject's `~/ros2_ws/src/`, clone this repo:
   ```bash
   cd ~/ros2_ws/src
   git clone <this-repo-url> lab
   cd ~/ros2_ws
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --symlink-install
   echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc
   echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
   ```
4. In the ROSject **Tools** menu, configure four launch entries (commands below). These give students one-click access:

   | Tool menu label | Command |
   |---|---|
   | Sim | `bash -lc 'ros2 launch lab sim.launch.py'` |
   | Teleop | `bash -lc 'ros2 run turtlebot3_teleop teleop_keyboard'` |
   | SLAM | `bash -lc 'ros2 launch lab slam.launch.py'` |
   | Nav2 | `bash -lc 'ros2 launch lab nav2.launch.py map:=$HOME/my_map.yaml'` |


---

## Files in detail

- **`lab/waypoint_follower.py`** — uses `nav2_simple_commander.BasicNavigator` to seed an initial pose and visit 4 waypoints. Print-statements show real-time progress (feedback distance remaining). Students can edit the `WAYPOINTS` list at the top.
- **`config/nav2_params.yaml`** — full Nav2 parameter set tuned for the TurtleBot3 burger. **Line ~XXX has the famous `inflation_radius: 0.55`** — comments next to it tell students exactly which line to edit for the bug-hunt buzzer stretch task.
- **`config/slam_params.yaml`** — online-async SLAM Toolbox config, sane defaults for the burger.
- **`maps/backup_map.yaml`** — a pre-made map of `turtlebot3_world` so the Nav2 hands-on still works if a student's SLAM map didn't save. **Generate this once** by running the SLAM block yourself and copying the saved files in.

---

## License

MIT. See `LICENSE`. Default upstream Nav2/SLAM/TurtleBot3 dependencies retain their own licenses.
