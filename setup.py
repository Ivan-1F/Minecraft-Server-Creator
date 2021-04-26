from setuptools import setup, find_packages
import os
import re

from mcservercreator import constants

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = [re.match(r'^[A-Za-z.]+', line).group() for line in f.readlines() if not len(line.strip()) == 0]

print('REQUIRED = {}'.format(REQUIRED))


setup(
    name=constants.PACKAGE_NAME,
    version=constants.VERSION,
    description=constants.DESCRIPTION,
    author=constants.AUTHOR,
    python_requires='>=3.6.0',
    url=constants.GITHUB_REPO,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    license='GPL-3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)