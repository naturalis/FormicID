###############################################################################
#                     __                      _      ___ ____                 #
#                    / _| ___  _ __ _ __ ___ (_) ___|_ _|  _ \                #
#                   | |_ / _ \| '__| '_ ` _ \| |/ __|| || | | |               #
#                   |  _| (_) | |  | | | | | | | (__ | || |_| |               #
#                   |_|  \___/|_|  |_| |_| |_|_|\___|___|____/                #
#                                                                             #
#                                      setup                                  #
#                                                                             #
###############################################################################

# Standard library imports
import io
import os
import sys
from shutil import rmtree

# Additional project imports
from setuptools import Command
from setuptools import find_packages
from setuptools import setup

try:
    import pypandoc

    long_description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    long_description = open("./README.md").read()


name = "FormicID"
description = "CNN-based image classification of AntWeb images."
url = "https://github.com/naturalis/FormicID"
email = "marijn.boer@naturalis.nl"
author = "Marijn J. A. Boer"
requires_python = ">=3.6.0"
version = None

with open('requirements.txt') as f:
    required = f.readlines()

# required = [
#     "Keras == 2.1.4",
#     "Pillow_SIMD == 4.3.0.post0",
#     "bunch == 1.0.1",
#     "graphviz == 0.8.2",
#     "h5py == 2.8.0rc1.post0",
#     "jmespath == 0.9.3",
#     "matplotlib == 2.2.2",
#     "numpy == 1.14.2",
#     "pandas == 0.22.0",
#     "pydot_ng == 1.0.0",
#     "pypandoc == 1.4",
#     "requests == 2.18.4",
#     "scikit_learn == 0.19.1",
#     "setuptools == 39.0.1",
#     "tensorflow == 1.7.0",
# ]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
if not version:
    with open(os.path.join(here, name, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = version


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system(
            "{0} setup.py sdist bdist_wheel --universal".format(sys.executable)
        )

        self.status("Uploading the package to PyPi via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=name,
    version=about["__version__"],
    description=description,
    long_description=long_description,
    author=author,
    author_email=email,
    python_requires=requires_python,
    url=url,
    packages=find_packages(exclude=("tests",)),
    install_requires=required,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    cmdclass={"upload": UploadCommand},
)
