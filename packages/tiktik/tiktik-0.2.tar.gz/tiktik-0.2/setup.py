from setuptools import setup,find_packages

setup(
    name='tiktik',
    version='0.2',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console-scripts":[
            "tiktik=tiktik:kavya",
        ],
    },
)