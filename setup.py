from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'auto_nav_antropi'


def tree(folder):
    out = []
    for root, _, files in os.walk(folder):
        if files:
            out.append((os.path.join('share', package_name, root),
                        [os.path.join(root, f) for f in files]))
    return out


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ] + tree('models'),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='karburettor',
    maintainer_email='whykarthikwhy@gmail.com',
    description='Autonomous Navigation with Turtlebot3',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={'console_scripts': []},
)