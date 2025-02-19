from setuptools import setup, find_packages

setup(
    name='reuse',
    version='0.0.1',
    packages=find_packages(where ='functions'),
    install_requires=[],
    author='Aayush Sugandhi',
    author_email='aayush.sugandhi@gmail.com',
    description='it has two functions to fetch and parse logs',
    long_description_content_type="text/markdown",
    keywords='just functions to reduce the use of some code',
    url='https://github.com/aayushsugandhi2703/minor_project',
    python_requires='>=3.6',
)