from setuptools import setup, find_packages

setup(
    name="pip_start",
    version="v0.1.2",
    author="Veillax",
    author_email="contact@veillax.com",
    description="A Python Package allowing thr automatic checking and updating of a python package upon import",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Veillax/pip_start", 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests"
    ],
)
