from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name="tilia",
	version="1.1.0",
	author="ralves-e",
	author_email="martins.ruiafonso@gmail.com",
	description="One more layer for pyautogui. Utilities for SAP integration.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	project_urls={
		"code": "https://github.com/rafonsomartins/tilia",
		"Example of Usage": "https://github.com/rafonsomartins/job_rar/tree/main/Automate%20SAP%20Assessment%20Cycle"
	},
    license="MIT License",
    Home_page="https://github.com/rafonsomartins/tilia",
	packages=find_packages(),
	install_requires=[
		"pyautogui",
		"pyperclip",
		"pygetwindow"
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires=">=3.6",
)
