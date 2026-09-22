from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    create_repub_share = get_package_share_directory("create3_republisher")

    return LaunchDescription(
    [
        # Create3 republisher
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    create_repub_share,
                    "bringup",
                    "create3_republisher_launch.py"
                )
            ),
            launch_arguments=[
                ("robot_ns", "/create3"),
                ("republisher_ns", "/"),
            ],
        ),

        # RealSense camera
        Node(
            package="realsense2_camera",
            executable="realsense2_camera_node",
            namespace="camera",
            name="camera",
            parameters=[
                {
                    "enable_color": True,
                    "enable_depth": False,
                    "pointcloud.enable": False,
                    "enable_accel": False,
                    "enable_gyro": False,
                    "unite_imu_topics": False,
                    "enable_infra1": False,
                    "enable_infra2": False,
                    "rgb_camera.color_profile": "960x540x30",
                }
            ],
        ),
    ]
)