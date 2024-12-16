from setuptools import setup, find_packages

setup(
    name="gunfireapi",  # The name of your package
    version="0.1.0",       # The version of your package
    packages=find_packages(),  # Automatically find and include all packages in the directory
    install_requires=[       # List of dependencies
        "requests",          # Add any dependencies here (e.g., requests)
    ],
    author="ihateapples",    # Your name
    author_email="contact@gunfire.icu",  # Your email
    description="python package to interact with the gunfire.icu file uploading api",  # Short description
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",  # File type of long description
    url="https://github.com/ihateapples/gunfireapi",  # Your project's URL (GitHub or other)
    classifiers=[          # Classifiers help people find your package on PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
