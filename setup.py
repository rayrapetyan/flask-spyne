"""
Flask-Spyne
~~~~~~~~~~~

Flask-Spyne is a `Flask <http://flask.pocoo.org>`_ extension which
provides `Spyne <http://spyne.io>`_ (formerly known as 
`soaplib <http://soaplib.github.io/soaplib/2_0/>`_) support.
Inspired by unofficial 
`Flask-Enterprise <http://massive.immersedcode.org/2011/staging/projects/default/python/flask-enterprise/>`_
extension (a wrapper on top of outdated `soaplib <http://soaplib.github.io/soaplib/2_0/>`_)

* `Documentation <https://pythonhosted.org/Flask-Spyne/>`_
* `PyPI listing <http://pypi.python.org/pypi/Flask-Spyne>`_
* `Source code repository <http://github.com/rayrapetyan/flask-spyne>`_

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
    description='A Flask extension, provides support for Spyne that makes it easy to expose online services that have a well-defined API using multiple protocols and transports.',
    download_url='http://pypi.python.org/pypi/Flask-Spyne',
    install_requires=requirements,
    include_package_data=True,
    keywords=['Flask', 'Spyne', 'soap', 'wsdl', 
            'wsgi', 'zeromq', 'rest', 'rpc', 'json', 'http',
            'msgpack', 'xml', 'sqlalchemy', 'werkzeug', 'yaml'],
    license='BSD',
    long_description=__doc__,
    name='Flask-Spyne',
    platforms='any',
    packages=['flask_spyne'],
    url='http://github.com/rayrapetyan/flask-spyne',
    version='0.1-dev',
    zip_safe=False
)
