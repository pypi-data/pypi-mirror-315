from setuptools import setup, find_packages

setup(
    name='komlos_optimal',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy'],
    description='Library for optimal subsequence computation inspired by Komlós conjecture.',
    author='Anthony Olevester',
    author_email='olevester.joram123@gmail.com',
    url='https://github.com/ANTHONY-OLEVESTER/komlos_optimal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
