import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-your-username",
    version="0.0.1",
    author="Yanni Etchi, Pascal Grosset",
    author_email="yannietchi@gmail.com, pascalgrosset@lanl.gov",
    description="An image comparator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lanl/libra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD 3",
        "Operating System :: OS Independent",
    ],
)