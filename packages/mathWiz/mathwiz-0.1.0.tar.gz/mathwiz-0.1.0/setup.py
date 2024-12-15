from setuptools import setup, find_packages

setup(
    name='mathWiz',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='This is a math module written in python, designed for math students or any programmers who wish to use complex math.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='William E.',
    author_email='williamemerick10@gmail.com',
    url='https://github.com/William-deg/mathWiz',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
