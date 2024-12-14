from distutils.core import setup
from setuptools import find_packages

setup(
    name='djongo-orm',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    author='Cherish',
    license='MIT',
    description='Djongo ORM',
    url='',
    install_requires=[
        'Django>=3.0.0',
        'djongo>=1.3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
