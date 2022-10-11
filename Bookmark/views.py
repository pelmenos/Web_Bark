from django.shortcuts import render, redirect
from django.views import View
from .models import Bookmarks


def index(request):
    return render(request, 'mark.html')


def AddBookmark(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        notes = request.POST.get('notes')
        author_id = request.user
        mark = Bookmarks(title=title, url=url, notes=notes, author=author_id)
        mark.save()
        return redirect('/')


class Delete_mark(View):
    def get(self, request, pk):
        mark = Bookmarks.objects.get(id=pk).delete()
        return redirect('/')
