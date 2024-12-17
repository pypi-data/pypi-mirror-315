from setuptools import setup, find_packages

setup(
    name="bayesian_network_generator",
    version="0.0.7",
    author="Rudzani Mulaudzi",
    author_email="rudzani@mulaudzi.co.za",
    description="A random bayesian network generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rudzanimulaudzi/bayesian_network_generator", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "pandas",
        "networkx",
        "pgmpy",
        "matplotlib",
    ],
    include_package_data=True,
)
