from flask import Flask

from flask_spyne import Spyne

from spyne.protocol.soap import Soap11

from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable

import logging

h = logging.StreamHandler()
rl = logging.getLogger()
rl.setLevel(logging.DEBUG)
rl.addHandler(h)

app = Flask(__name__)

spyne = Spyne(app)


class SomeSoapService(spyne.Service):
    __service_url_path__ = '/soap/someservice'
    __target_namespace__ = 'custom_namespace'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
    __wsse_conf__ = {
        'username': 'myusername',
        'password': 'mypassword'  # never store passwords directly in sources!
    }

    @spyne.srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def echo(str, cnt):
        for i in range(cnt):
            yield str


if __name__ == '__main__':
    app.run(host='0.0.0.0')
