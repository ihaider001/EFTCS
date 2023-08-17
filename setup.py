from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in eftc/__init__.py
from eftc import __version__ as version

setup(
	name="eftc",
	version=version,
	description="EFTC APP",
	author="NestorBird",
	author_email="info@nestorbird.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
