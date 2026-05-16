#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from people_msgs.msg import People
from visualization_msgs.msg import Marker, MarkerArray


class HumanMarkersNode(Node):

    def __init__(self):
        super().__init__("human_markers_node")

        self.sub = self.create_subscription(
            People,
            "/people",
            self.people_callback,
            10
        )

        self.pub = self.create_publisher(
            MarkerArray,
            "/human_markers",
            10
        )

        self.get_logger().info("Human markers node started")

    def create_zone_marker(
        self,
        frame_id,
        marker_id,
        x,
        y,
        radius,
        r,
        g,
        b,
        a,
        ns
    ):

        marker = Marker()

        marker.header.frame_id = frame_id
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = ns
        marker.id = marker_id

        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD

        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = 0.01

        marker.pose.orientation.w = 1.0

        marker.scale.x = radius * 2.0
        marker.scale.y = radius * 2.0
        marker.scale.z = 0.02

        marker.color.r = r
        marker.color.g = g
        marker.color.b = b
        marker.color.a = a

        return marker

    def people_callback(self, msg: People):

        markers = MarkerArray()

        for i, person in enumerate(msg.people):

            x = person.position.x
            y = person.position.y

            #
            # HUMAN BODY
            #

            human_marker = Marker()

            human_marker.header.frame_id = msg.header.frame_id
            human_marker.header.stamp = self.get_clock().now().to_msg()

            human_marker.ns = "humans"
            human_marker.id = i

            human_marker.type = Marker.SPHERE
            human_marker.action = Marker.ADD

            human_marker.pose.position.x = x
            human_marker.pose.position.y = y
            human_marker.pose.position.z = 0.8

            human_marker.pose.orientation.w = 1.0

            human_marker.scale.x = 0.4
            human_marker.scale.y = 0.4
            human_marker.scale.z = 1.6

            human_marker.color.r = 1.0
            human_marker.color.g = 0.2
            human_marker.color.b = 0.2
            human_marker.color.a = 0.9

            markers.markers.append(human_marker)

            #
            # INTIMATE ZONE
            #

            intimate_zone = self.create_zone_marker(
                frame_id=msg.header.frame_id,
                marker_id=1000 + i,
                x=x,
                y=y,
                radius=0.5,
                r=1.0,
                g=0.0,
                b=0.0,
                a=0.4,
                ns="intimate_zone"
            )

            markers.markers.append(intimate_zone)

            #
            # PERSONAL ZONE
            #

            personal_zone = self.create_zone_marker(
                frame_id=msg.header.frame_id,
                marker_id=2000 + i,
                x=x,
                y=y,
                radius=1.2,
                r=1.0,
                g=0.5,
                b=0.0,
                a=0.30,
                ns="personal_zone"
            )

            markers.markers.append(personal_zone)

            #
            # SOCIAL ZONE
            #

            social_zone = self.create_zone_marker(
                frame_id=msg.header.frame_id,
                marker_id=3000 + i,
                x=x,
                y=y,
                radius=2.0,
                r=0.0,
                g=1.0,
                b=0.0,
                a=0.20,
                ns="social_zone"
            )

            markers.markers.append(social_zone)

        self.pub.publish(markers)


def main(args=None):

    rclpy.init(args=args)

    node = HumanMarkersNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()