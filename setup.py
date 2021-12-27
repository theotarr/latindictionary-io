from setuptools import setup, find_packages

NAME = "latindictionary-io"
VERSION = "0.0.1"
REQUIRES = ["requests >= 2.22.0"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="latindictionary.io API",
    author="latindictionary.io",
    author_email="support@latindictionary.io",
    url="https://www.latindictionary.io/api/docs",
    keywords=["latin", "dictionary", "latin dictionary", "latindictionary.io", "latin api"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache-2.0",
    long_description=long_description,
    long_description_content_type="text/markdown"
)