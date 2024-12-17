from setuptools import setup, find_packages

# Dynamically retrieve the version
version = {}
with open("htree/__version__.py") as f:
    exec(f.read(), version)

setup(
    name='htree',
    version=version['__version__'],  # Dynamically load version
    packages=find_packages(),
    install_requires=[],
    description='A simple placeholder Python package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/htree',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
