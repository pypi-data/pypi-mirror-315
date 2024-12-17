# SPDX-License-Identifier: MIT
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neo-airpress",
    version="1.1.0",
    author="Jstyles",
    author_email="jstyles@styl.dev",
    description="A frustration-free compression tool for PKPass archives.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jontyms/neo-airpress",
    packages=["airpress"],
    install_requires=[
        "cryptography>=44.0.0",
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
