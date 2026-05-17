#include "agorabot_social_layer_cpp/social_layer.hpp"

#include <pluginlib/class_list_macros.hpp>
#include <cmath>

namespace agorabot_social_layer_cpp
{

SocialLayer::SocialLayer()
{
}

void SocialLayer::onInitialize()
{
  auto node = node_.lock();

  declareParameter("enabled", rclcpp::ParameterValue(true));

  node->get_parameter(name_ + "." + "enabled", enabled_);

  current_ = true;

  RCLCPP_INFO(
    node->get_logger(),
    "SocialLayer initialized");

  human_sub_ = node->create_subscription<hunav_msgs::msg::Agents>(
    "/human_states",
    10,
    std::bind(
      &SocialLayer::humansCallback,
      this,
      std::placeholders::_1));
}

void SocialLayer::humansCallback(
  const hunav_msgs::msg::Agents::SharedPtr msg)
{
  humans_ = msg;
}

void SocialLayer::updateBounds(
  double robot_x,
  double robot_y,
  double robot_yaw,
  double * min_x,
  double * min_y,
  double * max_x,
  double * max_y)
{
  if (!enabled_) {
    return;
  }

  *min_x = std::min(*min_x, robot_x - 10.0);
  *min_y = std::min(*min_y, robot_y - 10.0);
  *max_x = std::max(*max_x, robot_x + 10.0);
  *max_y = std::max(*max_y, robot_y + 10.0);
}

void SocialLayer::updateCosts(
  nav2_costmap_2d::Costmap2D & master_grid,
  int min_i,
  int min_j,
  int max_i,
  int max_j)
{
  if (!enabled_) {
    return;
  }

  if (!humans_) {
    return;
  }

  for (const auto & human : humans_->agents) {

    unsigned int mx, my;

    if (master_grid.worldToMap(
        human.position.position.x,
        human.position.position.y,
        mx,
        my))
    {
      int radius_cells = 20;

      for (int dx = -radius_cells; dx <= radius_cells; dx++) {

        for (int dy = -radius_cells; dy <= radius_cells; dy++) {

          int nx = static_cast<int>(mx) + dx;
          int ny = static_cast<int>(my) + dy;

          if (nx < 0 || ny < 0) {
            continue;
          }

          if (nx >= static_cast<int>(master_grid.getSizeInCellsX()) ||
              ny >= static_cast<int>(master_grid.getSizeInCellsY())) {
            continue;
          }

        //   double distance = std::sqrt(dx * dx + dy * dy);

        //   if (distance > radius_cells) {
        //     continue;
        //   }

        //   double normalized = distance / radius_cells;

        //   unsigned char cost =
        //     static_cast<unsigned char>((1.0 - normalized) * 252.0);

        double vx = human.velocity.linear.x;
        double vy = human.velocity.linear.y;

        double theta = 0.0;

        if (std::sqrt(vx * vx + vy * vy) > 0.05) {
        theta = std::atan2(vy, vx);
        }

        double local_x =
        std::cos(theta) * dx +
        std::sin(theta) * dy;

        double local_y =
        -std::sin(theta) * dx +
        std::cos(theta) * dy;

        double front_radius = 25.0;
        double side_radius = 12.0;
        double back_radius = 8.0;

        double a;

        if (local_x >= 0.0) {
        a = front_radius;
        } else {
        a = back_radius;
        }

        double ellipse_distance =
        std::sqrt(
            (local_x * local_x) / (a * a) +
            (local_y * local_y) / (side_radius * side_radius)
        );

        if (ellipse_distance > 1.0) {
        continue;
        }

        double normalized = ellipse_distance;

        unsigned char cost =
        static_cast<unsigned char>((1.0 - normalized) * 252.0);

          master_grid.setCost(nx, ny, cost);
        }
      }
    }
  }
}

void SocialLayer::reset()
{
  current_ = true;
}

}  // namespace agorabot_social_layer_cpp

PLUGINLIB_EXPORT_CLASS(
  agorabot_social_layer_cpp::SocialLayer,
  nav2_costmap_2d::Layer)