from setuptools import setup, find_packages

setup(
    name='htree',  # Change this to your desired package name
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # List dependencies here, e.g., ['numpy']
    description='A simple placeholder Python package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/htree',  # Update this
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
