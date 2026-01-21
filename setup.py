from setuptools import setup, find_packages

setup(
    name='CS3270',
    version='0.1',
    packages=find_packages(),
    description='Simple tool for analyzing weather data CSV',
    author='David Morse',
    author_email='dmmorse3@gmail.com',
    url='https://github.com/davidmorseiii/CS3270.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas',
    ],
)