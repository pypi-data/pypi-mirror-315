from setuptools import setup, find_packages

setup(
    name='skyshapython',
    version='0.3.1',
    packages=find_packages(),
    description='A Python library for utilities and wrappers for frequently used functionality.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sharangdeo Bhagwat',
    author_email='sharangdeo@protonmail.com',
    url='https://github.com/skywalker94/skyshapython',
    project_urls={
        'Bug Tracker': 'https://github.com/skywalker94/skyshapython/issues',
        'Source Code': 'https://github.com/skywalker94/skyshapython',
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],  # List of dependencies, if any
)