#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import Twist


class ChargingDriver(Node):

    def __init__(self):
        super().__init__('charging_driver')

        # TF
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(
            self.tf_buffer,
            self
        )

        # Velocity publisher
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Controller parameters
        self.target_distance = 0.10   # [m]
        self.k_linear = 0.5
        self.k_angular = 2.0

        # Control loop: 10 Hz
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

    def control_loop(self):

        try:
            trans = self.tf_buffer.lookup_transform(
                'base_link',
                'marker_19',
                rclpy.time.Time()
            )

        except Exception:
            self.get_logger().info('Marker not visible')

            # Stop robot if marker is lost
            self.cmd_pub.publish(Twist())
            return

        # Marker position relative to robot
        x = trans.transform.translation.x
        y = trans.transform.translation.y

        self.get_logger().info(
            f'Marker: x={x:.3f} m, y={y:.3f} m'
        )

        # Distance error
        error_x = x - self.target_distance

        cmd = Twist()

        # Stop when close enough
        if error_x <= abs(0.07):
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

            self.get_logger().info('Charging position reached')

        else:
            # Forward motion
            cmd.linear.x = self.k_linear * error_x

            # Steering correction
            cmd.angular.z = self.k_angular * y

            # Limit speeds
            cmd.linear.x = min(cmd.linear.x, 0.25)
            cmd.angular.z = max(
                min(cmd.angular.z, 0.5),
                -0.5
            )

        self.cmd_pub.publish(cmd)


def main():

    rclpy.init()

    node = ChargingDriver()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.cmd_pub.publish(Twist())

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()