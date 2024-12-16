from distutils.core import  setup
import setuptools
packages = ['is_pure_music']# 唯一的包名，自己取名
setup(name='is_pure_music',
	version='1.0',
	author='GGBoy',
    packages=packages,
    package_dir={'requests': 'requests'},)
