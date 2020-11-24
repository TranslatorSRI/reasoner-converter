"""Setup file for reasoner-converter package."""
from setuptools import setup

with open('README.md', 'r') as stream:
    long_description = stream.read()

setup(
    name='reasoner-converter',
    version='1.0.0',
    author='Patrick Wang',
    author_email='patrick@covar.com',
    url='https://github.com/NCATSTranslator/reasoner-converter',
    description='Version conversion tools for Reasoner API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['reasoner_converter'],
    install_requires=[],
    zip_safe=False,
    license='MIT',
    python_requires='>=3.6',
)
