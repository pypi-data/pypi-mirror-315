from setuptools import setup, find_packages
setup(
    name="fpe-library",
    version="0.1.0",
    author="Nehal Varma",
    author_email="nehalvarma85@gmail.com",
    description="Feature Probability Estimation-based Feature Selection Method",
    long_description="A Python library for Feature Probability Estimation and Feature Selection.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "scikit-learn>=0.22.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
