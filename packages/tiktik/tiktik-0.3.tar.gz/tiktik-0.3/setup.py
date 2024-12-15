from setuptools import setup,find_packages

setup(
    name='tiktik',
    version='0.3',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "tiktik_kavya=tiktik.main:kavya",
            "tiktik_kokul=tiktik.main:kokul",
        ],
    },
)