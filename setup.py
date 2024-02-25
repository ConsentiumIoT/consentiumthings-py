from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Python API for uploading data to Consentium IoT cloud'


# Setting up
setup(
    name="ConsentiumThings",
    version=VERSION,
    author="Consentium",
    author_email="<consentium.inc@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'communication', 'internet of things'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)