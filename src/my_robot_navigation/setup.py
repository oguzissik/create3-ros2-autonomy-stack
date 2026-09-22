import os
from glob import glob
from setuptools import setup


package_name = 'my_robot_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.*')),        
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
            'explorer_node = my_robot_navigation.auto_explorer:main'
        ],
    },
)
