from setuptools import setup, find_packages

setup(
    name='JakaModbusCommunication',                     # Your package name
    version='4.0.1',
    description='Modbus helper library for JAKA Cobot communication',
    author='Lucas Pijl',
    author_email='lapijl@uwaterloo.ca',
    packages=find_packages(),               # Automatically include package folders
    install_requires=['pymodbus'],          # Required libraries
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
