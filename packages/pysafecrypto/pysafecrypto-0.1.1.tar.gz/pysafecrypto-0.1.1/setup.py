from setuptools import setup, find_packages
setup(
    name='pysafecrypto',
    version='0.1.1',
    packages=find_packages(),
    python_requires='>=3.6',
    author='techscreed',
    author_email='techscreed@gmail.com',
    description='Python package for handling RSA encrption',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ScreedVA/pysafecrypto?tab=readme-ov-file',
    license='MIT'
)
