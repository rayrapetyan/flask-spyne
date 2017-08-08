from setuptools import setup

requirements = ['flask', 'spyne', 'sec-wall', 'pyyaml', 'lxml', 'suds-jurko', 'requests']

setup(
    author='Robert Ayrapetyan',
    author_email='robert.ayrapetyan@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='A Flask extension, provides support for Spyne.',
    long_description=open('README.rst').read(),
    download_url='http://pypi.python.org/pypi/Flask-Spyne',
    install_requires=requirements,
    include_package_data=True,
    keywords=['flask', 'spyne', 'soap', 'wsdl', 
            'wsgi', 'zeromq', 'rest', 'rpc', 'json', 'http',
            'msgpack', 'xml', 'werkzeug', 'yaml'],
    license='CC0 1.0',
    name='Flask-Spyne',
    platforms='any',
    packages=['flask_spyne'],
    url='http://github.com/rayrapetyan/flask-spyne',
    version='0.3.1',
    zip_safe=False
)
