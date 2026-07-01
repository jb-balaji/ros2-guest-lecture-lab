# Hands-on Lab Sheet — ROS 2 & Nav2 in 90 Minutes

> Print this 2-sided on one A4, or share the PDF.
> You will do **three short tasks**. Each has a **minimum success** step and a **stretch** for fast finishers. If you get stuck for more than 60 seconds, ask your group's screen captain.

---

## 0 · Setup (do this in the first 60 seconds)

1. Scan the QR on the projector or go to the short URL. Sign in (free Construct account).
2. Click **Open Rosject**. Wait ~30 s for the desktop to appear.
3. Sit in **groups of three**. Pick one **screen captain** — the person who will share their screen with the group if anyone falls behind.

> **Stuck on setup?** Skip ahead, watch a captain, you can catch up during Hands-on #2.
> **The Construct down?** The instructor will switch the projector to a local instance — you can follow along on the projected screen.

---

## 1 · First contact with ROS (12 min)

> **Goal:** drive the TurtleBot3 around with your own hands, and see what's underneath.

| # | Step | Type this | What to look for |
|---|------|-----------|------------------|
| 1 | Open a terminal. | Right-click desktop → **New Terminal** | A black box with a prompt. |
| 2 | List running nodes. | `ros2 node list` | A handful of node names. |
| 3 | List topics. | `ros2 topic list` | `/cmd_vel`, `/scan`, `/odom`, `/tf` should appear. |
| 4 | Open the Gazebo tool tab in the browser. | (one click in the **Tools** menu) | A small world with the TurtleBot3. |
| 5 | **Minimum success.** Open the **Teleop** terminal tab and drive the robot. | Click *inside* the terminal first, then use the keys it tells you (usually `w/a/s/d/x`). | The robot moves in Gazebo. |
| 6 | **Stretch.** Watch odometry. | In a new terminal: `ros2 topic echo /odom` | Numbers under `position` change as you drive. |

### Troubleshooting

- **Terminal won't open** → refresh the browser tab, the desktop will come back.
- **Gazebo is black / not loading** → close the Gazebo tab and reopen from the menu.
- **Teleop does nothing** → click *inside* the teleop terminal so it has keyboard focus.
- **Robot drives in circles only** → you're pressing the rotation key; the keymap is printed in the teleop terminal.

---

## 2 · Build & save your own map (10 min)

> **Goal:** drive the robot around and watch a map appear in real time. Save it for the next task.
> SLAM is **Cartographer** under the hood; the wrapping launch opens its own RViz pre-configured for mapping (Fixed Frame is already `map`).

| # | Step | Type this | What to look for |
|---|------|-----------|------------------|
| 1 | Stop the previous teleop session. | `Ctrl+C` in the teleop terminal. | Prompt returns. |
| 2 | Start SLAM (in a new terminal, with the workspace sourced). | `ros2 launch lab slam.launch.py` | A new RViz window opens; map starts filling as you drive. |
| 3 | Start teleop again (in another terminal). | `ros2 run turtlebot3_teleop teleop_keyboard` | You can drive again. |
| 4 | **Minimum success.** Drive *slowly* around the world. | Use teleop. | The map fills in: grey → white (free) and black (walls). |
| 5 | Save the map. | In a new terminal: `ros2 run nav2_map_server map_saver_cli -f ~/my_map` | Two files appear in your home directory: `my_map.yaml` and `my_map.pgm`. |
| 6 | **Stretch.** Force a loop closure. | Drive a full loop around the central feature of the world, then back to the start. | The map briefly snaps into better alignment as the loop closes. |

### Tips for a clean map

- **Drive slowly.** Sharp turns confuse SLAM.
- **Hug the walls.** Drive close enough to surfaces that the LiDAR can see them.
- **Don't skip rooms.** Anything you didn't drive past stays grey.
- If your save fails, you can still do §3 — it falls back to a pre-bundled map.

### Troubleshooting

- **RViz shows nothing** — drive ~30 cm so Cartographer accepts the first scan and publishes `/map`.
- **Map jumps around weirdly** — you drove too fast or rotated too hard. Drive back through the area slowly.
- **`map_saver_cli` says no map available** — Cartographer hasn't published `/map` yet; drive a bit more and retry.

---

## 3 · Send a goal, follow waypoints, break the costmap (15 min)

> **Goal:** use the full Nav2 stack — the same one that ships in real warehouse robots.

| # | Step | Type this | What to look for |
|---|------|-----------|------------------|
| 1 | Stop SLAM. | `Ctrl+C` in the SLAM terminal. | Prompt returns. |
| 2 | Launch Nav2 with your saved map. | `ros2 launch lab nav2.launch.py map:=$HOME/my_map.yaml` | RViz reopens with your map and a robot icon. |
| 3 | Tell Nav2 roughly where the robot is. | In RViz: click **2D Pose Estimate**, then click + drag near the robot's actual location, in its actual facing direction. | A red particle cloud collapses around the robot. |
| 4 | **Minimum success.** Send one goal. | In RViz: click **Nav2 Goal**, click anywhere reachable on the map. | Green global path appears; the robot drives along it. |
| 5 | Read the waypoint script with your neighbor. | `nano ~/ros_course/ros2_ws/src/lab/lab/waypoint_follower.py` (or open in the file browser). | ~50 lines of Python; the waypoint list is at the top. |
| 6 | Run it. | `ros2 run lab waypoint_follower` | The robot visits the 4 waypoints in order; progress prints in the terminal. |
| 7 | **Stretch A.** Add your own waypoints. | Edit the `WAYPOINTS` list in the script. Read coordinates off RViz by hovering. Save, rerun. | The robot visits your new waypoints. |
| 8 | **Stretch B — bug-hunt buzzer.** Break the costmap. | Open `~/ros_course/ros2_ws/src/lab/config/nav2_params.yaml`. Find the two `inflation_radius: 0.5` lines (commented *BUG-HUNT BUZZER*). Change both to `1.2`. Save, rebuild (`colcon build --symlink-install --packages-select lab && source install/setup.bash`), relaunch Nav2, try a goal in a tight corridor. | The goal is rejected or planning fails. **Why?** (First clear explanation wins a sticker.) |

### Reading the script (the 6 lines that matter)

```python
from nav2_simple_commander.robot_navigator import BasicNavigator

navigator = BasicNavigator()
navigator.setInitialPose(initial_pose)     # tell AMCL where you are
navigator.waitUntilNav2Active()            # wait for the stack to come up
navigator.followWaypoints(list_of_poses)   # send the goals
while not navigator.isTaskComplete():      # print feedback
    print(navigator.getFeedback())
```

This is the **5th concept** from the lecture — an **action**, hidden behind a friendly Python wrapper. Under the hood it's the same `NavigateThroughPoses` action that Nav2's BT Navigator listens on.

### Troubleshooting

- **`action server unavailable`** → Nav2 is still booting. Wait 5 s and rerun the script.
- **Robot doesn't move after goal** → AMCL probably isn't localized. Click **2D Pose Estimate** more carefully.
- **Planning fails immediately** → either inflation is too high (Stretch B) or the goal is inside an obstacle.
- **RViz is missing the map** → in RViz left panel, find *Map* display, ensure topic is `/map`.

---

## After the lecture

- Your ROSject **stays in your account**. Log back in any time.
- The 6 best next-step links are on the resources page (in the last slide and the post-lecture email).
- Email questions to the instructor — addresses on the final slide. Bonus karma if you send a screenshot of something cool you built.
