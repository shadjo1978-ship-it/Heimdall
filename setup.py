from setuptools import setup, find_packages

setup(
    name="heimdall",
    version="0.1.0",
    description="A.I. personal assistant with real time thinking and voice",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
)
