import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cmstk",
    version="0.1.0",
    author="Seaton Ullberg",
    author_email="sullberg@ufl.edu",
    description="Computational Materials Science Tool Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seatonullberg/cmstk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ]
)
