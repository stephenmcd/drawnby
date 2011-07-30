
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("core.views",
    url("^new/$", "drawing_new", name="new"),
    url("^view/(?P<slug>.*)/$", "drawing_view", name="view"),
    url("^all/$", "drawing_list", name="list"),
    url("^socket\.io", "socketio", name="socketio"),
    url("^auth/logout/$", "logout", name="logout"),
    url("^%s/$" % settings.LOGIN_REDIRECT_URL.strip("/"), "loggedin", name="loggedin"),
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
)
