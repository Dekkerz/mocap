from setuptools import find_packages, setup

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(
    name='mocap',
    packages=find_packages(),
    install_requires=requirements,
    version='0.0.2',
    description='Le Wagon MOCAP',
    author='Team MOCAP',
    license='MIT',
)
