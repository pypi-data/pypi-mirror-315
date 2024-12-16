from setuptools import setup, find_packages
setup(
    name="MobilTelesco",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "tifffile",
        "pytest",  # Include only if you want pytest as a dependency for testing
        "imageio",  # For reading and writing image files
        "pyexiv2",  # For reading and writing EXIF metadata
        "pandas",   # For data manipulation and analysis
    ],
)

classifiers=[ 
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],
description="An astrophotography image processing library",
long_description=open('README.md').read(), 
long_description_content_type='text/markdown',
author="Shantanu Parmar",
license="MIT"