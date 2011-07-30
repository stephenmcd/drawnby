
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    ("^%s/(?P<path>.*)$" % settings.MEDIA_URL.strip("/"),
        "django.views.static.serve", {"document_root":  settings.MEDIA_ROOT}),
)
