import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.6.9'
DESCRIPTION = 'Used to do scripting global variable proxy test tool'
LONG_DESCRIPTION = 'This software inherited from the previous version of the software, is a huge automation toolkit, mainly used for automated testing lazy tools'

# Setting up
setup(
    name="xiaoyu-proxy-pool",
    version=VERSION,
    author="小鱼程序员",
    author_email="732355054@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'computer vision', 'pyzjr','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)