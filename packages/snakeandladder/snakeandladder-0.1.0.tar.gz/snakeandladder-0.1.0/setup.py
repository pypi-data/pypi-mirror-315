from setuptools import setup, find_packages

setup(
    name="snakes-and-ladders",  # Replace with your package name
    version="0.1.0",  # Update version as needed
    author="Mohammed and Vidal",
    author_email="",  # Add a valid email address
    description="A snakes and ladders game package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohbay95/Project_533",  # Update with your GitHub repo URL
    packages=find_packages(),  # Automatically finds all packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  # Ensures package data files are included
    install_requires=[
        "Art",  # List all dependencies required for your project
    ],
)
