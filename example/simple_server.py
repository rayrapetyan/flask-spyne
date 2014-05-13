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
