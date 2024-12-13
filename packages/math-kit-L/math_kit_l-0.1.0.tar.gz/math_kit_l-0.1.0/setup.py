from setuptools import setup, find_packages

setup(
    name='math_kit_L',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add third-party dependencies here, if any
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lmcteam206?tab=repositories',
    author='lmc',
    author_email='lmcteam206@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
