import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='KennyPavan',
	version='v1.0.0',
	author="Kenny Pavan",
	author_email="pavan@protonmail.com",
	description="Kenny Pavan: About, projects, and resume as a PyPi package.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kennypavan/kennypavan",
	packages=setuptools.find_packages(where='src'),  
	package_dir={'': 'src'},  
	python_requires='>=3.7',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[],
)
