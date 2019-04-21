import os
from setuptools import setup

setup(
        name='structured_flask',
        version='1.0.0',
        license='MIT',
        author='Charles Ross',
        author_email='chivalry@mac.com',
        description='Starter project for Flask',
        packages=['app'],
        platform='any',
        install_requires=[
            'flask',
        ]
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development'
        ]
)
