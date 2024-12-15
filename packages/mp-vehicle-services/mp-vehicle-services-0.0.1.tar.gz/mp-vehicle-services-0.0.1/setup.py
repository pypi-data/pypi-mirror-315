
from setuptools import setup, find_packages


version = '0.0.1'
url = 'https://github.com/pmaigutyak/mp-vehicle-services'

setup(
    name='mp-vehicle-services',
    version=version,
    description='Django services app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
