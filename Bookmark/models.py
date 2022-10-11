from django.db import models
from django.urls import reverse


class Bookmarks(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', related_name='mark', on_delete=models.CASCADE, blank=True)

    def get_absolute_url(self):
        return reverse('delete_mark', kwargs={'pk': self.id})


