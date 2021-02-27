from setuptools import find_packages, setup

setup(
    name='mlaide',
    packages=find_packages(),
    install_requires=[
        'python-dateutil',
        'httpx',
        'cloudpickle',
        'dataclasses-json',
        'marshmallow'
    ],
    python_requires='>=3.8',
    version='0.0.1',
    description='This Python SDK integrates your Machine Learning Apps with ML Aide.',
    author='Ramandeep Singh & Farruch Kouliev',
    # license='?',
    # test_suite='tests',
)
