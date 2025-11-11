from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import Issue

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue


class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 10 # Optional pagination

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

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

