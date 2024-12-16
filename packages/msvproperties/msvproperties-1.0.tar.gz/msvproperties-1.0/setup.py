from setuptools import setup, find_packages

setup(
    name='msvproperties',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'certifi==2024.12.14',
        'charset-normalizer==3.4.0',
        'idna==3.10',
        'importlib==1.0.4',
        'numpy==2.2.0',
        'pandas==2.2.3',
        'probableparsing==0.0.1',
        'python-crfsuite==0.9.11',
        'python-dateutil==2.9.0.post0',
        'python-dotenv==1.0.1',
        'pytz==2024.2',
        'requests==2.32.3',
        'setuptools==75.6.0',
        'six==1.17.0',
        'tzdata==2024.2',
        'urllib3==2.2.3',
        'usaddress==0.5.11'
    ],
    description='A Library for using in our CRM',
    author='Alireza',
    author_email='alireza@msvproperties.net',
    url='https://github.com/alireza-msvproperties/msvproperties/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)