from setuptools import setup, find_packages

setup(
    name="istalktrance",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'numpy>=1.11.1'
    ],
    entry_points = {
        "console_scripts" : [ 
            "istalktrance-hello = istalktrance:example_function",
        ],
    },
)