from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.AddBookmark, name='add_mark'),
    path('delete/<int:pk>', views.Delete_mark.as_view(), name='delete_mark')
]
