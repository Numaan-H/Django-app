import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings

@require_POST
def set_weather_city(request):
    city = request.POST.get("city")

    if city:
        request.session["weather_city"] = city.strip()

    return redirect(request.META.get("HTTP_REFERER", "/"))

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5 # Optional pagination

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

def report(request):
   
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'contact'})

def report(request):
    # Get all reported issues
    issues = Issue.objects.all()

    # Create a context dictionary to pass to the template
    context = {'issues': issues}

    # Render the report.html template with the context
    return render(request, 'itreporting/report.html', context)

def weather_view(request):
    city_name = "York"   # you can make this dynamic later
    api_key = "2474636061ab426f55d6f07da1b3d43f"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_name}&appid={api_key}&units=metric"
    )

    response = requests.get(url)

    weather = None

    if response.status_code == 200:
        data = response.json()
        weather = {
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
        }

    return render(request, "base.html", {"weather": weather})
