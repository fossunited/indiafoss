from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in indiafoss/__init__.py
from indiafoss import __version__ as version

setup(
	name="indiafoss",
	version=version,
	description="Free and Open Source Software conference by the FOSS United community.",
	author="shridhar.p@zerodha..com",
	author_email="shridhar.p@zerodha..com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
