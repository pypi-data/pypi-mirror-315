#setup.py

from setuptools import setup, find_packages

setup(
    name='blogoapp',
    version='0.1',
    packages=find_packages(),
    description='A pipeline for question answering and retrieval-augmented generation (RAG)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gangadhar',
    author_email='gangadhartarun21@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
    'openai==0.28.0',
    'sentence-transformers==3.2.1',
    'faiss-cpu==1.9.0',
    'datasets==3.2.0',
    'transformers==4.46.3',
],
    python_requires='>=3.6',
)