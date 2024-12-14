from setuptools import setup, find_packages

setup(
    name='altikrity',
    version='0.6',
    packages=find_packages(),
    install_requires=[],
    author='Abdullah',
    author_email='abdullah.alttikrity@gmail.com',
    description='Lightweight encryption library with multi-layer encryption features.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
