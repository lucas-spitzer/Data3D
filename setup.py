from setuptools import setup, find_packages

setup(
    name='data3d',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'fake-bpy-module-4.0',
    ],
)