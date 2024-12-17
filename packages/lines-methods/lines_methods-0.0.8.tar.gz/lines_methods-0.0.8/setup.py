from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='lines-methods',
    version='0.0.8',
    author='UgryumovAV',
    author_email='ugriumov2102@gmail.com',
    description='This is the simplest module for quick work with 2D vectors',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/UgryumovAV',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    keywords='lines methods ',
    project_urls={
    'GitHub': 'https://github.com/UgryumovAV/lines_methods/'
    },
    python_requires='>=3.8'
)
