
from re import match
from thread import start_new_thread
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace

from core.utils import Actions


class DrawingNamespace(BaseNamespace, BroadcastMixin):

    def __init__(self, environ, ns_name, request=None):
        super(DrawingNamespace, self).__init__(environ, ns_name, request)
        self.actions = Actions(self)

    def on_message(self, message):
        broadcast = self.actions([str(s) for s in message])
        if broadcast:
            self.broadcast_event("message", message)


def application(environ, start_response):
    socketio_manage(environ, {"": DrawingNamespace})


class Command(BaseCommand):

    def handle(self, addrport="", **kwargs):
        if not addrport:
            self.addr = "127.0.0.1"
            self.port = 9000
        else:
            m = match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _, _, _, self.port = m.groups()
        server = SocketIOServer((self.addr, int(self.port)), application)
        server.serve_forever()
