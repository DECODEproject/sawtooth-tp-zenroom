
from setuptools import setup, find_packages

data_files = []

setup(
    name='sawtooth-zenroom',
    version="0.1.0",
    description='Zenroom Transaction Processor for Sawtooth',
    author='Dyne.org foundation',
    url='https://github.com/DECODEproject/sawtooth-tp-zenroom',
    packages=find_packages(),
    install_requires=[
        "cbor",
        "colorlog",
        "sawtooth-sdk",
        "sawtooth-signing",
        "zenroom==0.0.9",
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'zenroom-tp-cli = sawtooth_zenroom.client_cli.zenroom_cli:main_wrapper',
            'zenroom-tp-python = sawtooth_zenroom.processor.main:main'
        ]
    })
