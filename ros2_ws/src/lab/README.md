# `lab` package — student quick reference

This package is what you'll touch during the guest lecture. The big picture is in the top-level repo README and the lab sheet handout. This file is just a fast index.

## Run things

| Goal | Command |
|------|---------|
| Start Gazebo + TurtleBot3 | `ros2 launch lab sim.launch.py` |
| Teleop (drive with keys) | `ros2 run turtlebot3_teleop teleop_keyboard` |
| SLAM | `ros2 launch lab slam.launch.py` |
| Save the map | `ros2 run nav2_map_server map_saver_cli -f ~/my_map` |
| Nav2 with your map | `ros2 launch lab nav2.launch.py map:=$HOME/my_map.yaml` |
| Waypoint follower | `ros2 run lab waypoint_follower` |

## Files you might edit

- **`lab/waypoint_follower.py`** — change the `WAYPOINTS` list at the top.
- **`config/nav2_params.yaml`** — the famous `inflation_radius` is in two places (local and global costmap). Both are commented.

## What's the `TURTLEBOT3_MODEL` thing?

The TurtleBot3 packages need to know which model you're using (`burger`, `waffle`, or `waffle_pi`). Set it once per shell:

```bash
export TURTLEBOT3_MODEL=burger
```

Or persist it: `echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc`.
