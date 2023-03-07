from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Venkateswarareddy Dundi',
	author_email='venkateswarareddy.dundi-1@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)