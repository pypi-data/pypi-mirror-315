from setuptools import setup, find_packages

setup(
    name="ecraspay-py",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests >= 2.32.3",
        "pycryptodome >= 3.11.0",
    ],
    author="Asikhalaye Samuel",
    author_email="samuelasikhalaye@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    description="A Python wrapper for the ECRAS API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/thelimeskies/ecraspay-sdk/src/python",
)
