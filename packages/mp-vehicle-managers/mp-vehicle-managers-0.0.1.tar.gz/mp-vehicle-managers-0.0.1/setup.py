from setuptools import setup, find_packages

version = '0.0.1'
url = 'https://github.com/pmaigutyak/mp-vehicle-managers.git'

setup(
    name='mp-vehicle-managers',
    version=version,
    description='Django services app',
    author='Paul Maigutyak',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
