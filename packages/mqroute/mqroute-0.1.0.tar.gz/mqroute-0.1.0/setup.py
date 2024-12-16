from distutils.core import setup

setup(
    name='MQTTDeco',
    version='0.1.0',
    packages=['mqroute'],
    url='https://github.com/ehyde74/mqroute',
    license='MIT',
    author='ehyde74',
    author_email='',
    description="MQRoute is a Python library designed to simplify working "
                "with MQTT by providing advanced topic routing, "
                "asynchronous callback management, and decorator-based subscription.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "paho-mqtt>=2.1.0",
        "typeguard>=4.4.1",
        "pytest>=8.3.4"
    ],
)
