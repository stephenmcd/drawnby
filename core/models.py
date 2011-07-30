
from django.db import models


class Drawing(models.Model):

    users = models.ManyToManyField("auth.User")
    title = models.CharField(max_length=50)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def __unicode__(self):
        return self.title
