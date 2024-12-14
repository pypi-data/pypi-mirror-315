
from setuptools import setup, find_packages


version = '1.0.0'
url = 'https://github.com/pmaigutyak/mp-vehicle-customers'

setup(
    name='django-mp-vehicle-customers',
    version=version,
    description='Django customers app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
