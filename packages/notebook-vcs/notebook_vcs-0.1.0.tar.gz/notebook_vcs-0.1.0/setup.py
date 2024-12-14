from setuptools import setup, find_packages

setup(
    name="notebook_vcs",
    version="0.1.0",
    description="Version control system for Jupyter notebooks",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "notebook>=6.0.0",
        "ipython>=7.0.0",
        "nbformat>=5.0.0",
    ],
    include_package_data=True,
    data_files=[
        ('share/jupyter/nbextensions/notebook_vcs', [
            'notebook_vcs/static/main.js',
        ]),
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Jupyter",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
) 