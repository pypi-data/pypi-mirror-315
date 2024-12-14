from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name= 'BankingSystems',
    version='0.0.2',
    description='Basic ATM system with several features: deposit, withdrawal, transfer, balance checks',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ahriel, Fatim, Conner, Soto',
    author_email='ayoung08@rams.shepherd.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='banking system, ATM program',
    packages=find_packages(),
    install_requires=['tkinter']
)