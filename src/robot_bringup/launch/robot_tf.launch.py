from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_footprint_and_base_link',
            arguments=['0.0', '0.0', '0.01', '0.0', '0.0', '0.0',
                       'base_footprint', 'base_link']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_and_imu_link',
            arguments=['0.0', '0.0', '0.068', '0.0', '0.0', '0.0',
                       'base_link', 'imu_link']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_and_laser_frame',
            arguments=['0.0', '0.0', '0.15', '3.14159', '0.0', '0.0',
                       'base_link', 'laser_frame']
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_and_camera_link',
            arguments=['0.07', '0.0', '0.11', '0.0', '0.0', '0.0',
                       'base_link', 'camera_link']
        )
    ])
