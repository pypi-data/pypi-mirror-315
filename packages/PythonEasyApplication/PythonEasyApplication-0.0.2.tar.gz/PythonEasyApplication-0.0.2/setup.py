from setuptools import setup, find_packages
import os

requirements_path = "requirements.txt"

with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    name="PythonEasyApplication",
    version="0.0.2",
    description="Easy Application in Python",
    url='https://gitlab.com/lemon9693650/pythoneasyproject.git',
    author="ComiBesanaLevati",
    packages=find_packages(), 
    install_requires=dependencies,
)
