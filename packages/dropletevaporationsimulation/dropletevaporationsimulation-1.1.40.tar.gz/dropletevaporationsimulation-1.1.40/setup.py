from setuptools import setup, find_packages

setup(
    name="dropletevaporationsimulation",
    version="1.1.40",
    author="Guillaume Bailly",
    author_email="guillaume.bailly@estaca.eu",
    description="This project simulates the evaporation and dynamics of an n-Decane droplet in a heated airflow.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guillaume-bailly/DropletEvaporationSimulation",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
    ],
    entry_points={
        "console_scripts": [
            "des_run_simulation = src:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Minimum Python version
)
