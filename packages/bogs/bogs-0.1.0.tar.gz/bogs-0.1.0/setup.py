from setuptools import setup, find_packages

setup(
    name="bogs",  # Replace with your package name
    version="0.1.0",    # Version of your package
    description="A short description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Swaran66/TCRA_SRN",  # Your GitHub repository URL
    author="Your Name",
    author_email="your_email@example.com",
    license="MIT",  # Choose an appropriate license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Automatically find packages in your project
    python_requires=">=3.6",   # Minimum Python version
    install_requires=[
    ],
    include_package_data=True,  # Include non-code files from MANIFEST.in
)
