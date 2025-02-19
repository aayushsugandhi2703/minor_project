from setuptools import setup, find_packages

setup(
    name='parser-functions',  
    version='0.1.0',
    packages=find_packages(where='app'),  # Looks for packages inside "app/"
    package_dir={'': 'app'},  # Maps the root package directory to "app/"
    install_requires=[],  # Add dependencies if needed
    author='Aayush Sugandhi',
    author_email='aayush.sugandhi@gmail.com',
    description='Reusable functions for log parsing and processing',
    long_description_content_type="text/markdown",
    keywords='log parsing, authentication, flask',
    url='https://github.com/aayushsugandhi2703/minor-project',
    python_requires='>=3.6',
)
