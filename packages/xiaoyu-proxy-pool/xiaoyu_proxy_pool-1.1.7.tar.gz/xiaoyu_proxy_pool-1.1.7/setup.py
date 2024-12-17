import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.1.7'
DESCRIPTION = 'Used to do scripting global variable proxy test tool'
LONG_DESCRIPTION = 'Used to do scripting global variable proxy test tool, the tool can add ports and specified local production environment for local automation and multi-threaded batch interface testing '

# Setting up
setup(
    name="xiaoyu_proxy_pool",
    version=VERSION,
    author="小鱼程序员",
    author_email="3936775766@qq.com",
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