from setuptools import setup, find_packages

setup(
    name='sms8_api',
    version='0.1.8',  # Change the version number
    description='Opis Twojego pakietu',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Patryk',
    author_email='patryk.okonn@gmail.com',
    url='https://github.com/ryba-22/sms8_api',
    packages=find_packages(include=['sms8_api', 'sms8_api.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',  # Poprawna składnia - dodajemy nazwę pakietu jako ciąg znaków
    ],
)
