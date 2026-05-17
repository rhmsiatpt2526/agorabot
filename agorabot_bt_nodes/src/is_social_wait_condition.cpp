#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "behaviortree_cpp_v3/condition_node.h"
#include "behaviortree_cpp_v3/bt_factory.h"

class IsSocialWaitCondition : public BT::ConditionNode
{
public:
  IsSocialWaitCondition(
    const std::string & name,
    const BT::NodeConfiguration & config)
  : BT::ConditionNode(name, config)
  {
    config.blackboard->get("node", node_);

    sub_ = node_->create_subscription<std_msgs::msg::String>(
      "/social_behavior",
      10,
      [this](const std_msgs::msg::String::SharedPtr msg)
      {
        last_behavior_ = msg->data;
      });
  }

  static BT::PortsList providedPorts()
  {
    return {};
  }

  BT::NodeStatus tick() override
  {
    if (last_behavior_ == "WAIT") {
      return BT::NodeStatus::SUCCESS;
    }

    return BT::NodeStatus::FAILURE;
  }

private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
  std::string last_behavior_ = "NORMAL";
};

BT_REGISTER_NODES(factory)
{
  factory.registerNodeType<IsSocialWaitCondition>("IsSocialWait");
}