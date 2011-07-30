
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import DrawingForm
from core.models import Drawing


@login_required
def new(request, template="new.html"):
    form = DrawingForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            drawing = form.save()
            drawing.users.add(request.user)
            drawing.save()
            return redirect(drawing)
    context = {"form": form}
    return render(request, template, context)

@login_required
def view(request, slug, template="view.html"):
    drawing = get_object_or_404(Drawing, slug=slug)
    context = {"drawing": drawing}
    return render(request, template, context)

def loggedin(request):
    if request.user.is_authenticated():
        messages.success(request, "Logged in")
    return redirect(request.COOKIES.get("next", "home"))

def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
    messages.success(request, "Logged out")
    return redirect("home")
