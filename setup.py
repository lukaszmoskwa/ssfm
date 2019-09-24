import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssfm",
    version="0.0.1",
    author="Lykos94",
    author_email="lukaszmoskwa94@gmail.com",
    description="Curses based File Manager application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lykos94/ssfm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved ::GNU GPLv3 License",
        "Operating System :: Linux :: MacOS",
    ],
    python_requires='>=3.6',
)
