import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('auto_nav_antropi')
    nav2 = get_package_share_directory('nav2_bringup')

    map_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    # Gazebo + robot + bridge (without the old RViz)
    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'turtlebot3_world.launch.py')),
        launch_arguments={'use_rviz': 'false'}.items(),
    )

    # map_server, amcl, planner, controller, smoother, behaviors, bt_navigator, lifecycle manager
    nav = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': 'true',
            'autostart': 'true',
            'use_composition': 'False',
        }.items(),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', os.path.join(pkg, 'rviz', 'nav2.rviz')],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'map', default_value=os.path.join(pkg, 'maps', 'turtlebot_world_map.yaml')),
        DeclareLaunchArgument(
            'params_file', default_value=os.path.join(pkg, 'config', 'nav2_params.yaml')),
        sim,
        # Give Gazebo and /clock a few seconds before Nav2 starts
        TimerAction(period=5.0, actions=[nav]),
        TimerAction(period=6.0, actions=[rviz]),
    ])