# setup.py

from setuptools import setup, find_packages

setup(
    name="cifar-utils",  # Package name
    version="0.1.1",  # Version number
    packages=find_packages(),  
    install_requires=[],  # No dependencies needed
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    author='Jyothsna Lakshminarayanan',
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
)
