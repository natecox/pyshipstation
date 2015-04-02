import os
from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pyshipstation',
    author='Nathan Cox',
    author_email='akujin@akujin.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP'
    ],
    description='API bindings for the ShipStation API in Python',
    include_package_data=True,
    install_requires=['requests'],
    license='MIT',
    packages=['pyshipstation'],
    url='https://github.com/natecox/pyshipstation',
    version='0.1'
)
