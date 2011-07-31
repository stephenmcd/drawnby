
from os.path import join
from random import choice
from string import letters, digits

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from djangoratings.views import AddRatingFromModel
import redis

from core.forms import DrawingForm
from core.models import Drawing
from core.utils import Actions


def socketio(request):
    """
    Socket.IO handler.
    """
    socket = request.environ["socketio"]
    actions = Actions(socket)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                broadcast = actions(message)
                if broadcast:
                    socket.broadcast(message)
            else:
                if not socket.connected():
                    break
    except Exception, e:
        print e
    return HttpResponse("")

@login_required
def drawing_new(request):
    """
    Creates a new drawing key and redirects to the edit view for it.
    """
    drawing_key = "".join([choice(letters + digits) for i in range(6)])
    return redirect("edit", drawing_key)

def drawing_edit(request, drawing_key, template="edit.html"):
    """
    Edit a drawing.
    """
    context = {"drawing_key": drawing_key}
    return render(request, template, context)

def drawing_list(request, template="list.html"):
    """
    List all completed drawings.
    """
    context = {"drawings": Drawing.objects.all()}
    return render(request, template, context)

def drawing_view(request, slug, template="view.html"):
    """
    Display a drawing.
    """
    drawing = get_object_or_404(Drawing, slug=slug)
    context = {"drawing": drawing}
    return render(request, template, context)

def drawing_rate(request, drawing_id, score):
    """
    Wrap around djangorating's view so we can send a message and
    redirect back.
    """
    view = AddRatingFromModel()
    response = view(request, "drawing", "core", drawing_id, "rating", score)
    messages.success(request, response.content)
    return redirect(request.GET.get("next", "list"))

def login(request, template="login.html"):
    """
    Login - store the next param as a cookie since session may be lost.
    """
    context = {}
    response = render(request, template, context)
    response.set_cookie("next", request.GET.get("next", "home"))
    return response

def loggedin(request):
    """
    social-auth callback redirected to when user logs in.
    """
    if request.user.is_authenticated():
        messages.success(request, "Logged in")
    return redirect(request.COOKIES.get("next", "home"))

def logout(request):
    """
    Log out.
    """
    if request.user.is_authenticated():
        auth_logout(request)
    messages.success(request, "Logged out")
    return redirect("home")

def about(request, template="about.html"):
    """
    Convert the README file into HTML.
    """
    from docutils.core import publish_string
    from docutils.writers.html4css1 import Writer, HTMLTranslator
    writer = Writer()
    writer.translator_class = HTMLTranslator
    with open(join(settings.PROJECT_ROOT, "README.rst"), "r") as f:
        about = publish_string(f.read(), writer=writer)
    context = {"about": about}
    return render(request, template, context)
