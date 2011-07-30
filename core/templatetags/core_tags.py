
from django.template import Library

from core.models import Drawing


register = Library()

@register.filter
def photo_for_user(user):
    return "photos/%s" % user.id

@register.simple_tag(takes_context=True)
def load_in_progress(context):
    context["progress"] = Drawing.objects.filter(data__isnull=True)
    return ""
