from setuptools import setup, find_packages

setup(
    name='randomizer_package',
    version='0.6.0',
    packages=find_packages(),
    include_package_data=True,  # Include package data as specified in MANIFEST.in
    package_data={
        '': ['assets/frame0/*'],
    },
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'run_randomizer=randomizer.gui:main',
        ],
    },
    author='Nblancs',
    author_email='noeljhumel.blanco@1.ustp.edu.ph',
    description='A randomizer GUI application for generating random outputs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NBlancs/randomizer_nblancs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)