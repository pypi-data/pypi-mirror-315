# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comet_labs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'comet-labs',
    'version': '0.1.1',
    'description': 'A Python package for comet-related functionalities',
    'long_description': 'None',
    'author': 'Sahil',
    'author_email': 'sahil85.10s@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
