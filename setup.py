from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='PyFortiAPI',
    version='0.0.7',
    description='Python Wrapper for FortiGate API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='James Simpson',
    author_email='James@snowterminal.com',
    url='https://github.com/jsimpso/PyFortiAPI',
    license='MIT',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"

    ],
    keywords='fortigate fortios api',
    install_requires=['requests'],
    py_modules=["pyfortiapi"],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4'
)
