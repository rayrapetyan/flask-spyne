import logging

from werkzeug.wsgi import DispatcherMiddleware

from spyne.application import Application
from spyne.decorator import rpc, srpc
from spyne.service import ServiceBase, ServiceBaseMeta
from spyne.server.wsgi import WsgiApplication
from spyne.error import InvalidCredentialsError

from flask import _app_ctx_stack

from secwall import wsse
from secwall.core import SecurityException

from lxml import etree


class SpyneController(object):
    def __init__(self, app=None):
        self.services = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.real_wsgi_app = app.wsgi_app
        app.wsgi_app = self.wsgi_app

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['spyne'] = self

    def register_service(self, service):
        spyne_app = Application([service],
                                tns=service.__target_namespace__,
                                name=service.__name__,
                                in_protocol=service.__in_protocol__,
                                out_protocol=service.__out_protocol__)
        spyne_app.event_manager.add_listener('method_call',
                                             self._on_method_call)
        spyne_app.event_manager.add_listener('method_return_object',
                                             self._on_method_return_object)
        wsgi_app = WsgiApplication(spyne_app)
        self.services[service.__service_url_path__] = wsgi_app

    def wsgi_app(self, environ, start_response):
        dispatcher = DispatcherMiddleware(self.real_wsgi_app, self.services)
        return dispatcher(environ, start_response)

    def _on_method_call(self, ctx):
        if not _app_ctx_stack.top:
            appctx = self.app.app_context()
            ctx.udc = {"_spyne_ctx": appctx}
            appctx.push()
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
                    FSWSSE().validate(ctx.in_document, wsse_conf)
                except SecurityException as e:
                    logging.exception(e)
                    raise InvalidCredentialsError(e.description)

    def _on_method_return_object(self, ctx):
        logging.debug('response: {0}'.format(ctx.out_object))
        appctx = ctx.udc and ctx.udc.get("_spyne_ctx")
        if appctx:
            appctx.pop()


class SpyneService(ServiceBase):
    __target_namespace__ = 'tns'
    __service_url_path__ = '/rpc'


class FSWSSE(wsse.WSSE):
    def check_nonce(self, wsse_nonce, now, nonce_freshness_time):
        pass  # TODO


class Spyne(object):
    def __init__(self, app=None):
        self.app = app
        self.controller = SpyneController()

        class _BoundService(SpyneService):
            class __metaclass__(ServiceBaseMeta, type):
                def __new__(cls, name, bases, dict):
                    rv = type.__new__(cls, name, bases, dict)
                    if name != '_BoundService':
                        rv.controller = self.controller
                    return rv

                def __init__(cls, name, bases, dict):
                    ServiceBaseMeta.__init__(cls, name, bases, dict)
                    if name != '_BoundService':
                        self.controller.register_service(cls)

        self.Service = _BoundService
        self.srpc = srpc
        self.rpc = rpc

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.controller.init_app(app)
