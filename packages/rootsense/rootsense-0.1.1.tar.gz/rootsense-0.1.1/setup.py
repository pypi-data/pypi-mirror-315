from setuptools import setup, find_packages

setup(
    name="rootsense",  # Package name
    version="0.1.1",  # Version number
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[  # List of dependencies
        'pymongo',  # MongoDB client
        'reportlab',  # For generating PDF reports
        'psutil',
        'pandas',
        'numpy',
        'scikit-learn',
        'statsmodels',
        'prophet',
    ],
    entry_points={  # This section makes the `rootsense` command available
        'console_scripts': [
            'rootsense=rootsense.__main__:main',  # Ensure __main__.py exists and has a main() function
        ],
    },
    include_package_data=True,  # This ensures that non-Python files are included in the package
    description="A system performance and monitoring tool.",  # Short description of the package
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Format of README file
    url="https://github.com/yourusername/rootsense",  # Replace with your actual GitHub URL
    author="Your Name",  # Replace with your actual name
    author_email="your.email@example.com",  # Replace with your email
    license="MIT",  # License type, change if you use a different one
    classifiers=[  # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
