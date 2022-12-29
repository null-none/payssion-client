The Payssion API provides simple client for RESTful APIs

=======
Install
=======

.. code-block:: bash

    pip install payssion

=======
Example
=======

.. code-block:: python

    from payssion.src.api import Payssion

    API_KEY = 'API_KEY'
    APP_SECRET = 'APP_SECRET'
    payssion = Payssion(api_key=APP_CLIENT_ID, secrey_key=APP_SECRET, is_livemode=False)
    payssion.create({
    	'amount: 1,
	'currency': 'USD',
	'pm_id': 'alipay_cn',
	'description': 'order description',
	'order_id': 'your order id',
	'return_url': 'your return url'})

=======
Donation
=======

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
  :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YYZQ6ZRZ3EW5C
