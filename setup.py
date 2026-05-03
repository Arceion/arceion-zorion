#!/usr/bin/env python
"""
Setup script for Arceion package
"""

from setuptools import setup, find_packages

setup(
    name='arceion-zorion',
    version='0.1.0',
    description='Arceion Zorion - Django Microservices Framework',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Arceion',
    author_email='dev@arceion.io',
    url='https://github.com/Arceion/zorion',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'Django>=5.0',
        'djangorestframework>=3.14.0',
        'python-dotenv>=1.0.0',
        'pyyaml>=6.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-django>=4.5.2',
            'black>=23.0.0',
            'ruff>=0.1.0',
            'mypy>=1.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
