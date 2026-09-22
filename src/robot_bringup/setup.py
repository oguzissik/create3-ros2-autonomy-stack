import os
from glob import glob
from setuptools import setup

package_name = 'robot_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.*')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rss',
    maintainer_email='eb4626s@ad.fh-aachen.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tfnode = robot_bringup.static_transform_publisher:main',
            'aruconode = robot_bringup.aruco_node:main',
            'tf2_listener = robot_bringup.tf_listener:main',
            'driver_node =robot_bringup.charging_driver:main'
        ],
    },
)
