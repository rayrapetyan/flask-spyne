Flask-Spyne
===========

Flask-Spyne is a `Flask <http://flask.pocoo.org>`_ extension which
provides `Spyne <http://spyne.io>`_ (formerly known as 
`soaplib <http://soaplib.github.io/soaplib/2_0/>`_) support. 
Includes SOAP, WSDL, JSON, XML, YAML and other transports and protocols.
Inspired by unofficial 
`Flask-Enterprise <http://massive.immersedcode.org/2011/staging/projects/default/python/flask-enterprise/>`_
extension (a wrapper on top of outdated `soaplib <http://soaplib.github.io/soaplib/2_0/>`_).

* `PyPI listing <http://pypi.python.org/pypi/Flask-Spyne>`_

Installation
------------
::

    pip install flask-spyne

Please check `list of additional requirements <http://spyne.io/docs/2.11/#requirements>`_
you might need to install.

Server example
--------------

.. code-block:: python

  from flask import Flask
  from flask.ext.spyne import Spyne
  from spyne.protocol.soap import Soap11
  from spyne.model.primitive import Unicode, Integer
  from spyne.model.complex import Iterable
  
  app = Flask(__name__)
  spyne = Spyne(app)
  
  class SomeSoapService(spyne.Service):
      __service_url_path__ = '/soap/someservice'
      __in_protocol__ = Soap11(validator='lxml')
      __out_protocol__ = Soap11()
      
      @spyne.srpc(Unicode, Integer, _returns=Iterable(Unicode))
      def echo(str, cnt):
          for i in range(cnt):
              yield str
  
  if __name__ == '__main__':
      app.run(host = '127.0.0.1')

Client example
--------------

.. code-block:: python

  from suds.client import Client as SudsClient

  url = 'http://127.0.0.1:5000/soap/someservice?wsdl'
  client = SudsClient(url=url, cache=None)
  r = client.service.echo(str='hello world', cnt=3)
  print r

WS-Security
-----------

Starting from v0.2 flask-spyne supports basics of WS-Security for SOAP services.

Specify __wsse_conf__ dict with following fields::

    username (str, required)
    password (str, required)
    password-digest (bool, optional)
    nonce-freshness-time (int, optional)
    reject-empty-nonce-creation (bool, optional)
    reject-stale-tokens (bool, optional)
    reject-expiry-limit (int, optional)

See server_auth.py/client_auth.py in ``examples`` for more details.

Written by Robert Ayrapetyan (robert.ayrapetyan@gmail.com).

No copyright. This work is dedicated to the public domain.
For full details, see https://creativecommons.org/publicdomain/zero/1.0/

The third-party libraries have their own licenses, as detailed in their source files.
