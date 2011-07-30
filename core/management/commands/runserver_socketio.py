
from re import match

from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import naiveip_re
from socketio import SocketIOServer


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

        bind = (self.addr, int(self.port))
        print
        print "SocketIOServer running on %s:%s" % bind
        print
        server = SocketIOServer(bind, WSGIHandler(), resource="socket.io")
        server.serve_forever()
