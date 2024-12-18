from setuptools import setup, find_packages

# Read long description from README.md (optional but recommended)
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aes_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    description="A simple AES encryption and decryption module",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensures correct markdown format
    author="Aryan Mahajan",
    author_email="contact.aryan.mahajan@gmail.com",
    url="https://github.com/yourusername/aes_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can change this depending on your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust this based on the versions you support
    extras_require={
        "dev": ["pytest"],  # Add pytest for testing
    },
    test_suite="tests",  # Set the test suite directory for automatic discovery
)
