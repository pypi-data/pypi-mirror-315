from setuptools import setup, find_packages

setup(
    name='destinelab_test',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'PyJWT',
    ],
)
