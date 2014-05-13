"""

Flask-Spyne
===========

Flask-Spyne is a `Flask <http://flask.pocoo.org>`_ extension which
provides `Spyne <http://spyne.io>`_ (formerly known as 
`soaplib <http://soaplib.github.io/soaplib/2_0/>`_) support.
Inspired by unofficial 
`Flask-Enterprise <http://massive.immersedcode.org/2011/staging/projects/default/python/flask-enterprise/>`_
extension (a wrapper on top of outdated `soaplib <http://soaplib.github.io/soaplib/2_0/>`_).

* `Documentation <https://pythonhosted.org/Flask-Spyne/>`_
* `PyPI listing <http://pypi.python.org/pypi/Flask-Spyne>`_

Installation
------------
::

  pip install flask-spyne

Please check `list of additional requirements <http://spyne.io/docs/2.10/#requirements>`_ you might need to install.

Server example
---------------------

.. code-block:: python

  from flask import Flask
  from flask.ext.spyne import Spyne
  from spyne.protocol.soap import Soap11
  from spyne.model.primitive import Unicode, Integer
  from spyne.model.complex import Iterable
  
  app = Flask(__name__)
  spyne = Spyne(app)
  
  class SomeSoapService(spyne.service):
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

"""

from setuptools import setup

#: The installation requirements for Flask-Spyne.
requirements = ['flask', 'spyne']

setup(
    author='Robert Ayrapetyan',
    author_email='robert.ayrapetyan@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='A Flask extension, provides support for Spyne which supports SOAP, WSDL, JSON, XML and other protocols.',
    download_url='http://pypi.python.org/pypi/Flask-Spyne',
    install_requires=requirements,
    include_package_data=True,
    keywords=['flask', 'spyne', 'soap', 'wsdl', 
            'wsgi', 'zeromq', 'rest', 'rpc', 'json', 'http',
            'msgpack', 'xml', 'sqlalchemy', 'werkzeug', 'yaml'],
    license='BSD',
    long_description=__doc__,
    name='Flask-Spyne',
    platforms='any',
    packages=['flask_spyne'],
    url='http://github.com/rayrapetyan/flask-spyne',
    version='0.1',
    zip_safe=False
)
