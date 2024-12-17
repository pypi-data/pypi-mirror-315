
from setuptools import setup, find_packages

setup(
    name='pychow',
    version='0.1.0',
    author='Amir Babaei',
    author_email='pr.babayee@icloud.com',
    description='A Python implementation of the Chow Test for structural breaks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amirbabaei97/pychow',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'statsmodels',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
