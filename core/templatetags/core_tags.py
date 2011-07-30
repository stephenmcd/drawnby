
from django.template import Library


register = Library()

@register.filter
def photo_for_user(user):
    return "photos/%s" % user.id
