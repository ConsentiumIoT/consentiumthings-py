from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3'
DESCRIPTION = 'Python lib for sending sensor data to Consentium IoT server.'
LONG_DESCRIPTION = 'A package that allows to send sensor data to Consentium IoT server.'

# Setting up
setup(
    name="consentiumthings",
    version=VERSION,
    author="Debjyoti Chowdhury, Ph.D.",
    author_email="<consentium.inc@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['Python', 'Internet of Things'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)