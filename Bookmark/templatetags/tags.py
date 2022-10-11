from django import template

from Bookmark.models import Bookmarks

register = template.Library()


@register.simple_tag
def get_mark_list(id=0):
    return Bookmarks.objects.filter(author=id)
