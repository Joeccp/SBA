"""
Setup file

This file, and pyproject.toml, were originally created for publishing this project onto PyPI
(and for tox for workflow automation),
so that you can install this package with pip.

However, when I published it on TestPyPI for testing, I realized that
you will only install the SBA module inside the src folder,
not the whole SBA root directory.
I store all my data and log files inside folders that are up two levels of the directory of the SBA module.
It can't save anything.
It will crash.

It is too late for me to either change my program
or to do some research on how to configurate build/setuptools/wheel/twine.

But these two files are still useful.
They are needed by tox.
"""

# Copyright 2023 Joe Chau
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

if __name__ == '__main__':
	setup(
		name="SBA",
		author="Joe Chau",
		author_email="lmcs121005@gmail.com",
		description="A Cinema kiosk system for HKDSE ICT SBA project.",
		long_description="This is a Cinema Kiosk System project for "
		                 "the Hong Kong Diploma of Secondary Education Examination 2024 "
		                 "Information and Communication Technology "
		                 "Elective Part D - Software Development School-based Assessment. "
		                 "This project is a simple simulation of a cinema movie ticket system. "
		                 "This Cinema Kiosk System provides an easy way for customers to buy movie tickets. "
		                 "It also serves the administrator as a control platform."
		                 "Visit https://joeccp.github.io/SBA for more details.",
		url="https://github.com/Joeccp/SBA",
		classifiers=[  # https://pypi.org/classifiers/
			"Environment :: Console",
			"Environment :: Win32 (MS Windows)",
			"Intended Audience :: Customer Service",
			"License :: OSI Approved :: Apache Software License",
			"Natural Language :: Chinese (Traditional)",
			"Natural Language :: English",
			"Operating System :: Microsoft :: Windows :: Windows 10",
			"Operating System :: Microsoft :: Windows :: Windows 11",
			"Programming Language :: Python :: 3.11",
			"Programming Language :: Python :: 3.12",
			"Programming Language :: Python :: 3.13",
			"Topic :: Games/Entertainment :: Simulation",
			"Topic :: Software Development :: Embedded Systems",
			"Topic :: Software Development :: User Interfaces",
		]
	)
