from setuptools import setup, find_packages

# Read requirements from file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="RH_Package",  # Package name
    version="0.1.1",  # New Verion with little new features and bug fixes
    description="Package for RHI Metrics evaluation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Praveen Katwe, Naman Kabadi",
    author_email="c121007@iiit-bh.ac.in, namankabadi50@gmail.com",
    license="MIT",
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=requirements,  # Dependencies from requirements file
    python_requires=">=3.10",  # Minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Include other files (like README.md)
)
