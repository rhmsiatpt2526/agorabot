from setuptools import find_packages, setup

package_name = 'agorabot_social_layer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rhmsiatpt',
    maintainer_email='remi.hamon2022@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'human_markers_node = agorabot_social_layer.human_markers_node:main',
            'social_costmap_node = agorabot_social_layer.social_costmap_node:main',
            'social_behavior_node = agorabot_social_layer.social_behavior_node:main',
        ],
    },
)
