from setuptools import setup, find_packages

setup(
    name="stochPathSim",                        # Package name
    version="1.1.0",                           # Version
    author="Amit Kumar Jha",                   # Author's name
    author_email="jha.8@iitj.ac.in",           # Author's email
    description="A Python library for stochastic modeling and simulations.",
    long_description=open("README.md").read(), # Use README as long description
    long_description_content_type="text/markdown",
    url="https://github.com/AIM-IT4/stochPathSim",  # GitHub repo (create later)
    packages=find_packages(),                  # Automatically discover sub-packages
    include_package_data=True,                 # Include non-code files from MANIFEST.in
    install_requires=[
        "numpy>=1.20.0", 
        "pandas>=1.2.0", 
        "matplotlib>=3.3.0", 
        "plotly>=5.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                   # Minimum Python version
)
