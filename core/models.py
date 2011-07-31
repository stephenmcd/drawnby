
from os import mkdir
from os.path import join, exists
from urllib import urlretrieve

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from djangoratings.fields import RatingField
from social_auth.signals import socialauth_registered


class Drawing(models.Model):

    users = models.ManyToManyField("auth.User")
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = RatingField(range=5)

    class Meta:
        ordering = ("-id",)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("view", (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            i = 0
            self.slug = slugify(self.title)
            while True:
                if i > 0:
                    if i > 1:
                        self.slug = self.slug.rsplit("-", 1)[0]
                    self.slug = "%s-%s" % (self.slug, i)
                try:
                    Drawing.objects.exclude(id=self.id).get(slug=self.slug)
                except Drawing.DoesNotExist:
                    break
                i += 1
        super(Drawing, self).save(*args, **kwargs)

def create_profile(sender, user, response, details, **kwargs):
    try:
        # twitter
        photo_url = response["profile_image_url"]
        photo_url = "_reasonably_small".join(photo_url.rsplit("_normal", 1))
    except KeyError:
        # facebook
        photo_url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]
    path = join(settings.MEDIA_ROOT, "photos")
    if not exists(path):
        mkdir(path)
    urlretrieve(photo_url, join(path, str(user.id)))
socialauth_registered.connect(create_profile, sender=None)
