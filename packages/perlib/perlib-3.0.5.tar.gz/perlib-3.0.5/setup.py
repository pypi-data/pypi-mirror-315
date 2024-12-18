import setuptools
from setuptools import setup, find_packages
from perlib.__init__ import __version__

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

NAME = 'perlib'
VERSION = __version__
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = 'https://github.com/Ruzzg/perlib'
AUTHOR = 'Rüzgar Ersin Kanar'
DESCRIPTION = "Deep learning, Machine learning and Statistical learning for humans."
AUTHOR_EMAIL = 'ruzgarknr@gmail.com'
LICENSE = 'Apache Software License'
KEYWORDS = 'perlib,tensorflow,machine learning,deep learning,statistical learning,automl,autodl,modelselection'

# requirements.txt dosyasını oku
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='perlib',
    version=__version__,
    description="Deep learning, Machine learning and Statistical learning for humans.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/Ruzzg/perlib',
    author='Rüzgar Ersin Kanar',
    author_email='ruzgarknr@gmail.com',
    license='Apache Software License',
    install_requires=required,
    python_requires='>=3.10',
    keywords='perlib,tensorflow,machine learning,deep learning,statistical learning,automl,autodl,modelselection',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10',
    ],
)

