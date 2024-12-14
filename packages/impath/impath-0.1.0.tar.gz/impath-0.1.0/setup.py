from setuptools import setup, find_packages

setup(
    name="impath",                          # Package name
    version="0.1.0",                        # Initial version
    author="Mitchell Klusty",               # Author name
    author_email="mitchell.klusty@uky.edu", # Author email
    description="Pathology Imaging Tools",      # Short description
    long_description=open("README.md").read(),  # Long description (optional)
    long_description_content_type="text/markdown",  # README content type
    url="https://github.com/innovationcore/path_tools_lib",  # Project URL
    packages=find_packages(),               # Automatically discover modules
    install_requires=[           # Dependencies
        "opencv-python>=4.5.0",  # For computer vision tasks
        "numpy>=1.21.0",         # For numerical computations
        "requests>=2.26.0",      # For HTTP requests
        "pillow>=8.0.0",         # For image processing
        # Optional:
        # "opencv-contrib-python>=4.5.0",
        # "pillow-simd>=8.0.0; platform_machine=='x86_64'",
    ],
    classifiers=[                           # Metadata classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",                # Minimum Python version
)