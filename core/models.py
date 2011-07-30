
from django.db import models
from django.template.defaultfilters import slugify


class Drawing(models.Model):

    users = models.ManyToManyField("auth.User")
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("view", (self.slug,))

    def save(self, *args, **kwargs):
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
