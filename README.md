# Autonomous Navigation with TurtleBot3 (ROS 2 Jazzy + Gazebo Harmonic + Nav2)

A TurtleBot3 Burger navigates autonomously to goals in a Gazebo world while avoiding obstacles, using the Nav2 stack, AMCL localisation and a map built with SLAM Toolbox.

**Demo video:** https://drive.google.com/file/d/1TCPS0_3zTSQef8gqoGVi2J_jiXgR5kHB/view?usp=sharing

## Tested on
- Ubuntu 24.04, ROS 2 Jazzy, Gazebo Sim 8 (Harmonic), Nav2 1.3.x

## Prerequisites
```bash
sudo apt install -y ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-slam-toolbox ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations \
  ros-jazzy-ros-gz ros-jazzy-xacro ros-jazzy-teleop-twist-keyboard
```

## Build
```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/whykarthikwhy/turtlebot3-nav2-gazebo.git auto_nav_antropi
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## Environment setup (every new terminal)
```bash
source ~/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(ros2 pkg prefix auto_nav_antropi)/share/auto_nav_antropi/models
```
- `TURTLEBOT3_MODEL=burger` selects the TurtleBot3 Burger variant used by the TurtleBot3 packages.
- `GZ_SIM_RESOURCE_PATH` tells Gazebo Harmonic where to find this package's `models/` folder, so `model://` references in the world file resolve.

To make this permanent:
```bash
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(ros2 pkg prefix auto_nav_antropi)/share/auto_nav_antropi/models' >> ~/.bashrc
```

## Run: autonomous navigation
```bash
ros2 launch auto_nav_antropi navigation.launch.py
```
This starts Gazebo with the world, the robot, the ROS-Gazebo bridge, Nav2 (map server, AMCL, planner, controller, behaviours, BT navigator) and RViz.

In RViz, click **2D Goal Pose**, then click and drag on the map. The robot plans a path and drives around the obstacles to the goal. The initial pose is already set to the spawn point (0, 0); use **2D Pose Estimate** if the scan looks misaligned.

## Run: simulation only (teleop)
```bash
ros2 launch auto_nav_antropi turtlebot3_world.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Rebuild the map (optional)
```bash
ros2 launch auto_nav_antropi turtlebot3_world.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run nav2_map_server map_saver_cli -f src/auto_nav_antropi/maps/turtlebot_world_map --ros-args -p use_sim_time:=true
```

## Package layout
| Path | Purpose |
|---|---|
| `launch/turtlebot3_world.launch.py` | Gazebo + robot + bridge + RViz |
| `launch/navigation.launch.py` | Simulation + Nav2 + Nav2 RViz view |
| `worlds/turtlebot_world.sdf` | House world with sensor plugins and obstacles |
| `maps/` | Saved occupancy-grid map |
| `config/nav2_params.yaml` | Nav2 parameters tuned for the TurtleBot3 Burger |
| `rviz/` | RViz configs |

## Notes
- The robot is spawned from the official `turtlebot3_gazebo` SDF model (diff-drive, joint-state, lidar and IMU plugins). `robot_state_publisher` uses the URDF only for TF.
- `ros_gz_bridge` bridges `/clock`, `/cmd_vel`, `/odom`, `/joint_states`, `/scan`, `/imu` and `/tf`.
- All nodes run with `use_sim_time: true`.
