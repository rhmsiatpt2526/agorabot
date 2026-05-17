#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from hunav_msgs.msg import Agents
from std_msgs.msg import String

from nav_msgs.msg import Odometry


class SocialBehaviorNode(Node):

    def __init__(self):

        super().__init__("social_behavior_node")

        self.humans = None
        self.robot_x = 0.0
        self.robot_y = 0.0

        self.create_subscription(
            Agents,
            "/human_states",
            self.humans_callback,
            10
        )

        self.create_subscription(
            Odometry,
            "/mobile_base_controller/odom",
            self.odom_callback,
            10
        )

        self.behavior_pub = self.create_publisher(
            String,
            "/social_behavior",
            10
        )

        self.timer = self.create_timer(
            0.2,
            self.update_behavior
        )

        self.get_logger().info(
            "Social behavior node started"
        )

    def humans_callback(self, msg):

        self.humans = msg

    def odom_callback(self, msg):

        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def update_behavior(self):

        if self.humans is None:
            return

        behavior = "NORMAL"

        close_humans = 0

        for human in self.humans.agents:

            hx = human.position.position.x
            hy = human.position.position.y

            dx = hx - self.robot_x
            dy = hy - self.robot_y

            distance = math.sqrt(dx * dx + dy * dy)

            #
            # Count nearby humans
            #

            if distance < 1.2:

                close_humans += 1

        #
        # SOCIAL DECISION LOGIC
        #

        if close_humans >= 3:

            behavior = "TRAPPED"

        elif close_humans >= 1:

            behavior = "WAIT"

        else:

            behavior = "NORMAL"

        msg = String()
        msg.data = behavior

        self.behavior_pub.publish(msg)

        self.get_logger().info(
            f"Social behavior: {behavior}"
        )

def main(args=None):

    rclpy.init(args=args)

    node = SocialBehaviorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()