
import redis

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import DrawingForm
from core.models import Drawing


pool = redis.ConnectionPool()

def socketio(request):
    """
    Socket.IO handler.
    """
    socket = request.environ["socketio"]
    r = redis.Redis(connection_pool=pool)
    try:
        while True:
            message = socket.recv()
            if len(message) > 0:
                drawing_id, action = message[:2]
                drawing_key = "drawing-%s" % drawing_id
                user_key = "users-%s" % drawing_id
                if action == "join":
                    # Add the user to the user set.
                    r.sadd(user_key, ",".join(message[2:]))
                    # Get all users with args prepended to look like join actions.
                    user_actions = [s for m in r.smembers(user_key) for s in [drawing_id, "join"] + m.split(",")]
                    # Get all the draw actions.
                    drawing_actions = [s for m in r.lrange(drawing_key, 0, -1) for s in m.split(",")]
                    # Dump the combined action list to the joining user.
                    socket.send(drawing_actions + user_actions)
                elif action == "leave":
                    # Remove the user from the user set.
                    r.srem(user_key, ",".join(message[2:]))
                else:
                    # Add the draw action.
                    r.rpush(drawing_key, ",".join(message))
                socket.broadcast(message)
            else:
                if not socket.connected():
                    break
    except Exception, e:
        print e
    return HttpResponse("")

@login_required
def drawing_new(request, template="new.html"):
    """
    Creates a new drawing.
    """
    form = DrawingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            drawing = form.save()
            drawing.users.add(request.user)
            drawing.save()
            messages.success(request, "Drawing created")
            return redirect(drawing)
    context = {"form": form}
    return render(request, template, context)

@login_required
def drawing_view(request, slug, template="view.html"):
    """
    Display a drawing.
    """
    drawing = get_object_or_404(Drawing, slug=slug)
    context = {"drawing": drawing}
    return render(request, template, context)

def drawing_list(request, template="list.html"):
    """
    List all drawings.
    """
    context = {"drawings": Drawing.objects.all()}
    return render(request, template, context)

def login(request, provider):
    """
    Login - store the next param as a cookie since session may be lost.
    """
    response = redirect("begin", provider)
    response.set_cookie("next", request.GET.get("next", ""))
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
