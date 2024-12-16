from distutils.core import setup
from setuptools import find_packages

setup(
    name='djongo_orm',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    author='Cherish',
    author_email='',
    license='MIT',
    description='Djongo ORM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    install_requires=[
        'Django>=3.0.0',
        'djongo>=1.3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
