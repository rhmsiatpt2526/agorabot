#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from people_msgs.msg import People
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose


class SocialCostmapNode(Node):

    def __init__(self):

        super().__init__("social_costmap_node")

        self.sub = self.create_subscription(
            People,
            "/people",
            self.people_callback,
            10
        )

        self.pub = self.create_publisher(
            OccupancyGrid,
            "/social_costmap",
            10
        )

        #
        # COSTMAP PARAMETERS
        #

        self.width = 200
        self.height = 200

        self.resolution = 0.05

        self.origin_x = -5.0
        self.origin_y = -5.0

        self.get_logger().info("Social costmap node started")

    def people_callback(self, msg: People):

        grid = OccupancyGrid()

        #
        # HEADER
        #

        grid.header.frame_id = msg.header.frame_id
        grid.header.stamp = self.get_clock().now().to_msg()

        #
        # MAP INFO
        #

        grid.info.resolution = self.resolution

        grid.info.width = self.width
        grid.info.height = self.height

        grid.info.origin.position.x = self.origin_x
        grid.info.origin.position.y = self.origin_y
        grid.info.origin.orientation.w = 1.0

        #
        # EMPTY GRID
        #

        data = [0] * (self.width * self.height)

        #
        # FOR EACH HUMAN
        #

        for person in msg.people:

            human_x = person.position.x
            human_y = person.position.y

            #
            # LOOP OVER GRID
            #

            for y in range(self.height):

                for x in range(self.width):

                    #
                    # CELL POSITION IN WORLD
                    #

                    world_x = self.origin_x + x * self.resolution
                    world_y = self.origin_y + y * self.resolution

                    #
                    # DISTANCE TO HUMAN
                    #

                    dx = world_x - human_x
                    dy = world_y - human_y

                    distance = math.sqrt(dx * dx + dy * dy)

                    #
                    # SOCIAL COST
                    #

                    cost = 0

                    #
                    # INTIMATE ZONE
                    #

                    if distance < 0.5:
                        cost = 100

                    #
                    # PERSONAL ZONE
                    #

                    elif distance < 1.2:
                        cost = 70

                    #
                    # SOCIAL ZONE
                    #

                    elif distance < 2.0:
                        cost = 40

                    #
                    # WRITE COST
                    #

                    index = y * self.width + x

                    data[index] = max(data[index], cost)

        grid.data = data

        self.pub.publish(grid)


def main(args=None):

    rclpy.init(args=args)

    node = SocialCostmapNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()