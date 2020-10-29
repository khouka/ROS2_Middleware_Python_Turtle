from setuptools import setup

package_name = 'webcam'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='khoukhi',
    maintainer_email='khoukhi@todo.todo',
    description='ROS 2 Webcam publisher and Subscriber',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'webcam_pub_node = webcam.webcam_pub:main',
                'webcam_sub_node = webcam.webcam_sub:main',
        ],
    },
)
