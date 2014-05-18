from setuptools import setup

requirements = ['flask', 'spyne', 'sec-wall', 'pyyaml']

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
    description='A Flask extension, provides support for Spyne.',
    long_description=open('README.txt').read(),
    download_url='http://pypi.python.org/pypi/Flask-Spyne',
    install_requires=requirements,
    include_package_data=True,
    keywords=['flask', 'spyne', 'soap', 'wsdl', 
            'wsgi', 'zeromq', 'rest', 'rpc', 'json', 'http',
            'msgpack', 'xml', 'sqlalchemy', 'werkzeug', 'yaml'],
    license='BSD',
    name='Flask-Spyne',
    platforms='any',
    packages=['flask_spyne'],
    url='http://github.com/rayrapetyan/flask-spyne',
    version='0.2',
    zip_safe=False
)
