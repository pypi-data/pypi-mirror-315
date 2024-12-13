from setuptools import setup, find_packages

setup(
    name="ars_dev",  # Package name
    version="0.1.0",  # Package version
    author="Yu-Jen Chiu",  # Author name
    author_email="yoshi_chiu@berkeley.edu",  # Author email
    description="A JAX/numpy implementation of Adaptive Rejection Sampling (ARS) introduced by Gilks and Wild in 1992",  # Short description
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.berkeley.edu/yoshi-chiu/ars-dev",  # Project URL
    packages=find_packages(),  # Automatically find subpackages
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",  # Python version requirement
    install_requires=["numpy>=1.26.4", # dependencies
                      "jax>=0.4.26",
                      "jaxlib>=0.4.0",
                      "scipy>=1.7.0",
                      "seaborn>=0.11.0",
                      "matplotlib>=3.4.0",
                      "pytest>=7.0.0",
                      "numdifftools>=0.9.0",
                      ],  
)
