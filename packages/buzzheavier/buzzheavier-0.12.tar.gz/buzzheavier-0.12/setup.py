# author     : Hadi Cahyadi
# email      : cumulus13@gmail.com
# description: BUzzheavier link generator
# created in 20 minutes :)
# -*- coding: UTF-8 -*-

import io
from setuptools import setup, find_packages

# Read the README file
with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

version = {}
with open("__version__.py") as fp:
    exec(fp.read(), version)

version = version['version']

setup(
    name="buzzheavier",
    version=version,
    url="https://github.com/cumulus13/buzzheavier",
    project_urls={
        "Documentation": "https://github.com/cumulus13/buzzheavier",
        "Code": "https://github.com/cumulus13/buzzheavier",
    },
    license="GPL",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Buzzheavier link generator",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'argparse',
        'rich',
        'configset',
        'ctraceback',
        'pydebugger',
        'requests',
        'bs4',
        'parserheader',
        'clipboard'
    ],
    entry_points={
        "console_scripts": [
            "buzz = buzzheavier.__main__:usage",
            "buzzheavier = buzzheavier.__main__:usage",
        ]
    },
    data_files=['__version__.py', 'README.md', 'LICENSE.md'],
    license_files=["LICENSE.md"],    
    include_package_data=True,
    python_requires=">=3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License (GPL)', 
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
