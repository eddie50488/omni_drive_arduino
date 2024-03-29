from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("omni_drive_arduino"), "urdf", "omnibot.urdf.xacro"]
            ),
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    robot_controller = PathJoinSubstitution(
        [
            FindPackageShare("omni_drive_arduino"),
            "config",
            "omni_controller_config.yaml",
        ]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, robot_controller],
        output="both",
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "omnidirectional_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="both",
    )

    nodes = [
        control_node,
        robot_controller_spawner,
    ]

    return LaunchDescription(nodes)
