from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, weather_view, set_weather_city, email_signup, module_detail,  module_list
from users.views import contact_view, profile, profile_edit


app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact/', contact_view, name='contact'),
    path('report/', PostListView.as_view(), name = 'report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issues/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    path("set-city/", set_weather_city, name="set_weather_city"),
    path("modules/", views.module_list, name="module_list"),
    path("modules/<str:code>/", views.module_detail, name="module_detail"),
]