from setuptools import setup, find_packages

setup(
    name='wqdab',
    version='0.0.6',
    description='This is a pre-alpha package that contains benchmark for water quality monitoring.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Victor Henrique Alves Ribeiro',
    author_email='vhrique@gmail.com',
    url='https://github.com/vhrique/wqdab',
    packages=find_packages(),
    install_requires=[
        'prts>=1.0.0.3', 'scikit-learn>=1.5.2', 'pandas>=2.2.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
