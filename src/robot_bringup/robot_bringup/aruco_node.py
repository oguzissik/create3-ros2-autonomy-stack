#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ArucoNode(Node):

    def __init__(self):
        super().__init__('aruco_node')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_5X5_100
        )

        self.parameters = cv2.aruco.DetectorParameters()

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        corners, ids, rejected = cv2.aruco.detectMarkers(
            frame,
            self.aruco_dict,
            parameters=self.parameters
        )

        if ids is not None:
            self.get_logger().info(f'ArUco IDs: {ids.flatten().tolist()}')


def main():
    rclpy.init()
    node = ArucoNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
