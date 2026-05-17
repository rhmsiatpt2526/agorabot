#include "agorabot_social_layer_cpp/social_layer.hpp"

#include "pluginlib/class_list_macros.hpp"

namespace agorabot_social_layer_cpp
{

SocialLayer::SocialLayer()
{
}

void SocialLayer::onInitialize()
{
  current_ = true;
}

void SocialLayer::updateBounds(
  double,
  double,
  double,
  double * min_x,
  double * min_y,
  double * max_x,
  double * max_y)
{
}

void SocialLayer::updateCosts(
  nav2_costmap_2d::Costmap2D & master_grid,
  int min_i,
  int min_j,
  int max_i,
  int max_j)
{
}

void SocialLayer::reset()
{
}

}  // namespace agorabot_social_layer_cpp

PLUGINLIB_EXPORT_CLASS(
  agorabot_social_layer_cpp::SocialLayer,
  nav2_costmap_2d::Layer)