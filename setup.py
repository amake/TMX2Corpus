from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tmx2corpus',
    version='1.0',
    description='Convert TMX files to bilingual corpora (for MT, etc.)',
    long_description=long_description,
    url='https://github.com/amake/tmx2corpus',
    author='Aaron Madlon-Kay',
    author_email='aaron@madlon-kay.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Pre-processors',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='tmx corpus conversion',
    py_modules=['tmx2corpus', 'tokenizer', 'filter'],
    install_requires=['tinysegmenter'],
    entry_points={
        'console_scripts': [
            'tmx2corpus=tmx2corpus:main',
        ],
    },
    test_suite='./tmx2corpus_test.TestTMX2Corpus',
)
