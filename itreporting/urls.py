from django.urls import path
from . import views
from .views import PostListView, PostDetailView


app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact', views.contact, name='contact'),
    path('report/', PostListView.as_view(), name = 'report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
]