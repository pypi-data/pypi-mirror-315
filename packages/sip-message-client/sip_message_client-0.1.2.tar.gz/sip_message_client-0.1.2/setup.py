# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sip_message_client', 'sip_message_client.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sip-message-client',
    'version': '0.1.2',
    'description': 'simple python socket app to send sms via sip server',
    'long_description': '# sip_message\nsip client to send message to asterisk\n\n# example use\n\n```python\nsip_client = SipClient("10.0.0.15", 5060, "sipuser", "password")\nresponse = sip_client.message.send("+48555222111", "test message")\n```\n\n\n# command line install\n```\ncmd/install_command_line.sh\n```\n\n# command line usage \n```\nsip_message --server=10.0.0.15 --username=sipuser --password=password --recipient=+48555222111 --message="test message"`\n```\n\n',
    'author': 'Przemyslaw Bubas',
    'author_email': 'bprzemys@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
