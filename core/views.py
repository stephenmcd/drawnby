
from random import choice
from string import letters, digits

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import redis

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
                drawing_key, action = message[:2]
                drawing_data_key = "drawing-%s" % drawing_key
                user_data_key = "users-%s" % drawing_key
                if action == "join":
                    # Add the user to the user set.
                    r.sadd(user_data_key, ",".join(message[2:]))
                    # Get all users with args prepended,
                    # to look like join actions.
                    user_actions = [s for m in r.smembers(user_data_key)
                                    for s in [drawing_key, "join"] + m.split(",")]
                    # Get all the draw actions.
                    drawing_actions = [s for m in r.lrange(drawing_data_key, 0, -1)
                                       for s in m.split(",")]
                    # Dump the combined action list to the joining user.
                    socket.send(user_actions + drawing_actions)
                elif action == "leave":
                    # Remove the user from the user set.
                    r.srem(user_data_key, ",".join(message[2:]))
                    # Remove the drawing actions if last user.
                    if len(r.smembers(user_data_key)) == 0:
                        r.delete(drawing_data_key)
                elif action == "save":
                    drawing = Drawing.objects.create(title=message[2], data=message[3].replace(" ", "+"))
                    for user in r.smembers(user_data_key):
                        drawing.users.add(User.objects.get(id=user.split(",")[1]))
                    continue
                else:
                    # Add the draw action.
                    r.rpush(drawing_data_key, ",".join(message))
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

def login(request, provider):
    """
    Login - store the next param as a cookie since session may be lost.
    """
    response = redirect("begin", provider)
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
