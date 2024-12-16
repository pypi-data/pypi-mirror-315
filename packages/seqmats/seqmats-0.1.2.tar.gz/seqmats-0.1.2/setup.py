from setuptools import setup

setup(
    name='seqmats',
    version='0.1.2',
    description='A small python package to make handling genomic sequences and manipulations a bit quicker.',
    url='https://github.com/shuds13/pyexample',
    author='Nicolas Lynn',
    author_email='nicolasalynn@gmail.com',
    license='Free for non-commercial use',
    packages=['seqmats'],
    install_requires=['numpy',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.9',
    ],
)