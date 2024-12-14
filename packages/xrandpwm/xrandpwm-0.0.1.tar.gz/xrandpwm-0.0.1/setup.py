from setuptools import setup, find_packages

setup(
    name="xrandpwm",
    version="0.0.1",
    packages=find_packages(),
    description="xrandr screen/monitors info collector classes (intended for bspwm)",
    author="kokaito",
    author_email="kokaito.git@gmail.com",
    url="https://github.com/kokaito-git/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "pydantic",
        "kcolors",
    ],
)
