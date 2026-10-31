import os
from launch import LaunchDescription
#from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
#from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration


def generate_launch_description():
    pkg = get_package_share_directory('auto_nav_antropi')
    tb3_gz = get_package_share_directory('turtlebot3_gazebo')
    tb3_desc = get_package_share_directory('turtlebot3_description')

    # Lets Gazebo resolve model:// URIs (meshes/materials) used by the TB3 SDF
    set_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH', os.path.join(tb3_gz, 'models'))

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': '-r ' + os.path.join(pkg, 'worlds', 'turtlebot_world.sdf')
        }.items(),
    )

    # URDF is now only used for TF (robot_state_publisher); Gazebo uses the SDF
    robot_desc = ParameterValue(
        Command(['xacro ', os.path.join(tb3_desc, 'urdf', 'turtlebot3_burger.urdf'),
                 ' namespace:=""']),
        value_type=str)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
        output='screen',
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'turtlebot3_burger',
                   '-file', os.path.join(tb3_gz, 'models', 'turtlebot3_burger', 'model.sdf'),
                   '-x', '0.0', '-y', '0.0', '-z', '1.0'],
        output='screen',
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
        ],
        output='screen',
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_rviz')),
        parameters=[{'use_sim_time': True}],
        arguments=['-d', os.path.join(pkg, 'rviz', 'turtlebot.rviz')],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_rviz', default_value='true'),
        set_resources,
        gz_sim,
        robot_state_publisher,
        ros_gz_bridge,
        spawn_robot,
        rviz2,
    ])