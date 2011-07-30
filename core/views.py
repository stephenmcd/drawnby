
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
                users_key = "users-%s" % drawing_id
                if action == "join":
                    # Add the user to the user set.
                    r.sadd(users_key, ",".join(message[2:]))
                    # Get all users with args prepended,
                    # to look like join actions.
                    user_actions = [s for m in r.smembers(users_key)
                                    for s in [drawing_id, "join"] + m.split(",")]
                    # Get all the draw actions.
                    drawing_actions = [s for m in r.lrange(drawing_key, 0, -1)
                                       for s in m.split(",")]
                    # If there are no actions, check to see if the drawing
                    # data has been saved, and create the initial load
                    # action for the data.
                    if not drawing_actions:
                        drawing = Drawing.objects.get(id=drawing_id)
                        if drawing.data:
                            drawing_actions = [drawing_id, "load", drawing.data]
                            r.rpush(drawing_key, ",".join(drawing_actions))
                    # Dump the combined action list to the joining user.
                    socket.send(user_actions + drawing_actions)
                elif action == "leave":
                    image = message.pop(2)
                    # Remove the user from the user set.
                    r.srem(users_key, ",".join(message[2:]))
                    # Store the image data if no more users.
                    if len(r.smembers(users_key)) == 0:
                        drawing = Drawing.objects.get(id=drawing_id)
                        drawing.data = image.replace(" ", "+")
                        drawing.save()
                        r.delete(drawing_key)
                elif action == "save":
                    drawing = Drawing.objects.get(id=drawing_id)
                    drawing.data = message[2].replace(" ", "+")
                    drawing.save()
                    continue
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
    List all completed drawings.
    """
    context = {"drawings": Drawing.objects.filter(data__isnull=False)}
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
