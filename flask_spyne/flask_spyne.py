"""

Provides Spyne support to Flask
2014 Robert Ayrapetyan <robert.ayrapetyan@gmail.com>
License: BSD

"""

import logging

from werkzeug.wsgi import DispatcherMiddleware

from spyne.application import Application
from spyne.decorator import rpc, srpc
from spyne.service import ServiceBase, ServiceBaseMeta
from spyne.server.wsgi import WsgiApplication

from secwall import wsse
from secwall.core import SecurityException

from lxml import etree

from spyne.model.fault import Fault
# TODO: use native spynes' InvalidCredentialsError (after ver > 2.10 release)
class InvalidCredentialsError(Fault):
    """Raised when requested resource is forbidden."""
    STR = "You do not have permission to access this resource"
    def __init__(self, fault_string=STR, fault_object=None):
        super(InvalidCredentialsError, self).__init__(
            'Client.InvalidCredentialsError', fault_string, detail=fault_object)

class SpyneController(object):
    def __init__(self, app):
        self.app = app
        self.services = {}
        self.real_wsgi_app = app.wsgi_app
        app.wsgi_app = self.wsgi_app
        
    def register_service(self, service):        
        spyne_app = Application([service], 
            tns=service.__target_namespace__,
            name=service.__name__,
            in_protocol=service.__in_protocol__,
            out_protocol=service.__out_protocol__)
        wsgi_app = WsgiApplication(spyne_app)
        self.services[service.__service_url_path__] = wsgi_app
        
    def wsgi_app(self, environ, start_response):
        dispatcher = DispatcherMiddleware(self.real_wsgi_app, self.services)
        return dispatcher(environ, start_response)

class SpyneService(ServiceBase):
    __target_namespace__ = 'tns'
    __service_url_path__ = '/rpc'
    
class FSWSSE(wsse.WSSE):
    def check_nonce(self, wsse_nonce, now, nonce_freshness_time):
        pass # TODO

def _on_method_call(ctx):
    logging.debug('request: {0}'.format(ctx.in_object))
    if ctx.service_class.__in_protocol__.__class__.__name__ == 'Soap11':
        logging.debug('request: {0}'.format(etree.tostring(ctx.in_document, pretty_print=True)))
        if hasattr(ctx.service_class, '__wsse_conf__'):
            def_conf = {
                'reject-empty-nonce-creation': False,
            }
            wsse_conf = dict(def_conf.items() + ctx.service_class.__wsse_conf__.items())
            for k, v in wsse_conf.items():
                wsse_conf['wsse-pwd-{0}'.format(k)] = v
            try:               
                auth_res = FSWSSE().validate(ctx.in_document, wsse_conf) 
            except SecurityException as e:
                logging.exception(e)
                raise InvalidCredentialsError(e.description)
    return

def _on_method_return_object(ctx):
    logging.debug('response: {0}'.format(ctx.out_object))

SpyneService.event_manager.add_listener('method_call', _on_method_call)
SpyneService.event_manager.add_listener('method_return_object', _on_method_return_object)

def make_spyne_controller(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    rv = app.extensions['spyne'] = SpyneController(app)
    return rv

class Spyne(object):
    def __init__(self, app):        
        self.app = app        
        self.controller = make_spyne_controller(app)      

        class _BoundService(SpyneService):        
            class __metaclass__(ServiceBaseMeta, type):
                def __new__(cls, name, bases, dict):                    
                    rv = type.__new__(cls, name, bases, dict)                    
                    if name != '_BoundService':
                        # weird: "self" points to "Spyne" instance here...
                        rv.controller = self.controller                        
                    return rv
                def __init__(cls, name, bases, dict):
                    ServiceBaseMeta.__init__(cls, name, bases, dict)
                    if name != '_BoundService':
                        self.controller.register_service(cls)
        
        self.Service = _BoundService
        self.srpc = srpc
        self.rpc = rpc
