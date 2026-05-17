#include "agorabot_social_layer_cpp/social_layer.hpp"

#include <pluginlib/class_list_macros.hpp>

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
      master_grid.setCost(
        mx,
        my,
        nav2_costmap_2d::LETHAL_OBSTACLE);
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