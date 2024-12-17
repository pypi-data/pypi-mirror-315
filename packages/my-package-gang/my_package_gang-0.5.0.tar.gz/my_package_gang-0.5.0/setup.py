from setuptools import setup, find_packages

setup(
    name='my_package_gang',
    version='0.5.0',
    packages=find_packages(),
    install_requires=[],
    author='gang',
    description='A simple calculator package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
