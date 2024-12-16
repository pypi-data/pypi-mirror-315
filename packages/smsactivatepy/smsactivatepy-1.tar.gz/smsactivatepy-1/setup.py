import setuptools

with open(r'README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='smsactivatepy',
	version='1',
	author='Gabriel Lima',
	author_email='gabrielmrts@yahoo.com',
	description='smsactivatepy is an Python module that provides functions for working with the API sms-activate.org',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['smsactivatepy'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
