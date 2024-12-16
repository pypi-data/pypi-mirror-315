from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="opennano",
    version="0.1.0",
    author="Charalampos Anagostakis, Laura Beltrame, Cristiano Cordì, and Niamh Callian Keenan",
    author_email="charalampos.anagnostakis@student.kuleuven.be, laura.beltrame@student.kuleuven.be",
    description="A Python package for processing NanoString GeoMx data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Niamhck/opennano",
    project_urls={
        "Documentation": "https://opennano.pages.dev/",
        "Bug Tracker": "https://github.com/Niamhck/opennano/issues",
        "Source Code": "https://github.com/username/opennano",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    package_dir={"": "opennano"},
    packages=find_packages(where="opennano"),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "anndata>=0.8.0",
        "scipy>=1.6.0",
    ],
    include_package_data=True,
    license="MIT",
    keywords="nanostring geomx spatial transcriptomics bioinformatics",
)