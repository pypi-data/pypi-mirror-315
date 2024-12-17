from setuptools import setup, find_packages

setup(
    name='statsy',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    license='Apache License 2.0',
    description='A package of statistical functions and operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)