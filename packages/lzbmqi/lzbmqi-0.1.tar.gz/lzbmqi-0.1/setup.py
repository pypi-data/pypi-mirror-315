from setuptools import setup, find_packages

setup(
    name='lzbmqi',
    version='0.1',
    description="A simple Python package",
    author='Zephyr',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires=">=3.6",
)

