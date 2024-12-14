from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

long_description = (HERE / "README.md").read_text()

setup(
    name="hosty",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "urwid",
    ],
    entry_points={
        "console_scripts": [
            "hosty = hosty:main",
        ],
    },
    author="ctrlpy",
    author_email="ctrlpy@example.com",
    description="A simple utility for managing hostnames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CtrlPy/hosty",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
