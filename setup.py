import os

from setuptools import find_packages
from setuptools import setup


def path_in_project(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def read_file(filename):
    with open(path_in_project(filename)) as f:
        return f.read()


def read_requirements(filename):
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []

setup(
    name="yawsm",
    version="0.0.1",
    author="Maciej Walerczuk",
    author_email="mwalerczuk@gmail.com",
    description="yawsm",
    license="BSD",
    packages=find_packages(include=path_in_project('yawsm*'), exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'yawsm = yawsm.app:main',
        ],
    },
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('requirements_dev.txt'),
    zip_safe=False,
)
