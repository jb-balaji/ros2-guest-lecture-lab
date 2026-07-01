# Backup map of `turtlebot3_world`

A pre-made map is bundled here so the Nav2 hands-on (§3) still works even if a
student's own SLAM save fails:

- `backup_map.yaml`
- `backup_map.pgm`

Use it directly:

```bash
ros2 launch lab nav2.launch.py map:=$(ros2 pkg prefix lab)/share/lab/maps/backup_map.yaml
```

## Regenerating it

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch lab sim.launch.py
ros2 launch lab slam.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
# drive around until the map is complete, then:
ros2 run nav2_map_server map_saver_cli -f backup_map
# copy backup_map.yaml + backup_map.pgm back into this folder and commit them
```
