#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sentry>=6.0.0',
]

f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='sentry-export',
    version='0.8.1',
    author='Dave McLain',
    author_email='dmclain@gmail.com',
    url='http://github.com/dmclain/sentry-export',
    description='A Sentry extension for exporting event data',
    long_description=readme,
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'sentry.apps': [
            'sentry_export = sentry_export',
            ],
        'sentry.plugins': [
            'sentry_export = sentry_export.plugin:ExportPlugin'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
)
