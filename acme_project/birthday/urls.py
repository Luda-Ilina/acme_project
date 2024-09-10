from django.urls import path

from . import views_old_funcs

app_name = 'birthday'

urlpatterns = [
    path('', views_old_funcs.birthday, name='create'),
    path('list/', views_old_funcs.birthday_list, name='list'),
    path('<int:pk>/edit/', views_old_funcs.birthday, name='edit'),
    path('<int:pk>/delete/', views_old_funcs.delete_birthday, name='delete'),
]
