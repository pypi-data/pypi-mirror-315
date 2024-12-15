import pathlib
from setuptools import setup

setup(
    name="TensorflowImageHelperCD",
    version="0.1.0",
    description="Helper package for TensorFlow IMAGE CNN and DNN and Display image (dummy)",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/SA-Ahmed-W/TensorflowImageHelperCD",
    author="saaw",
    author_email="aasimahmedsiddiqui45666@gmail.com",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
