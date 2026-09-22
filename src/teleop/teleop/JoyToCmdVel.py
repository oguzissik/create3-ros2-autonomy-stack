from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import rclpy
from rclpy.node import Node


class JoyToCmdVel(Node):

  def __init__(self):
    super().__init__('JoyToCmdVel')
    self.publisher_ = self.create_publisher(Twist, '/create3/cmd_vel', 10)
    self.subscription = self.create_subscription(
        Joy, '/joy', self.joy_callback, 10
    )

    # Define which button acts as the deadman switch (e.g., button index 4)
    self.deadman_button_index = 4
    self.emg_button_index = 5

  def joy_callback(self, msg: Joy):
    twist = Twist()

    # Ensure indices are within bounds of the received message
    has_deadman = len(msg.buttons) > self.deadman_button_index
    has_emg = len(msg.buttons) > self.emg_button_index

    # 1. Priority: If the emergency button is pressed, stop immediately
    if has_emg and msg.buttons[self.emg_button_index] == 1: # 1 means button is pressed 0 is not pressed
      twist.linear.x = 0.0
      twist.angular.z = 0.0
    # 2. If the deadman switch is held down, allow movement
    elif has_deadman and msg.buttons[self.deadman_button_index] == 1:
      twist.linear.x = float(msg.axes[1])  # Left stick vertical
      twist.angular.z = float(msg.axes[0])  # Left stick horizontal
    # 3. Default fallback: nothing pressed, stop the robot
    else:
      twist.linear.x = 0.0
      twist.angular.z = 0.0

    # Publish the command
    self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = JoyToCmdVel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()