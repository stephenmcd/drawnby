
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect


def loggedin(request):
    if request.user.is_authenticated():
        messages.success(request, "Logged in")
    return redirect(request.COOKIES.get("next", "home"))

def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
    messages.success(request, "Logged out")
    return redirect("home")
