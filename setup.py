from setuptools import setup, find_packages

setup(
    name="ws_dist_queue",
    version="0.0.1",
    author="Maciej Walerczuk",
    author_email="mwalerczuk@gmail.com",
    description="ws_dist_queue",
    license="BSD",
    keywords="example documentation tutorial",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'queue = ws_dist_queue.work.cli:queue',
        ],
    },
)
