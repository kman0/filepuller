__author__ = 'M'
from setuptools import setup
import codecs

long_description = codecs.open("README.md", encoding='utf-8').read()

VERSION = '0.1'
PYPI_VERSION = '0.1'

setup(
    name='filepuller',
    description='pull and replace remote files',
    long_description=long_description,
    version=VERSION,
    url='https://github.com/manojklm/filepuller/',
    download_url='https://github.com/manojklm/filepuller/tarball/%s' % PYPI_VERSION,
    license='MIT',
    author='mk',
    author_email='manojklm@gmail.com',
    zip_safe=False,
    packages = ['filepuller'],
    include_package_data=True,
    platforms='any',
    install_requires=['path.py'],
    classifiers=[
        'Environment :: Plugins',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
