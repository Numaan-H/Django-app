import requests
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from users.models import Profile
from .models import Issue, Course, Module, Student
from users.forms import StudentRegistrationForm, UserUpdateForm, ProfileUpdateForm, EmailSignupForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required  

@require_POST
def set_weather_city(request):
    city = request.POST.get("city")

    if city:
        request.session["weather_city"] = city.strip()

    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def course_list(request):
    courses = Course.objects.all().order_by("code")
    return render(request, "itreporting/course_list.html", {"courses": courses})

@login_required
def course_detail(request, code):
    course = get_object_or_404(Course, code=code)
    modules = course.modules.all().order_by("code")
    return render(
        request,
        "itreporting/course_detail.html",
        {"course": course, "modules": modules},
    )

@login_required
def module_list(request):
    modules = Module.objects.filter(is_open=True)
    return render(request, "itreporting/module_list.html", {
        "modules": modules
    })

@login_required
def module_detail(request, code):
    module = get_object_or_404(Module, code=code)
    student = request.user.student


    is_registered = module.students.filter(id=student.id).exists()

    if request.method == "POST" and module.is_open:
        if is_registered:
            module.students.remove(student)
        else:
            module.students.add(student)

    return render(request, "itreporting/module_detail.html", {
        "module": module,
        "is_registered": is_registered,
    })


def my_modules(request):
    student = request.user.student

    modules = Module.objects.all()

    if request.method == "POST":
        module_id = request.POST.get("module_id")
        action = request.POST.get("action")  
        module = get_object_or_404(Module, id=module_id)

        if module.is_open:
            if action == "register":
                module.students.add(student)
            elif action == "unregister":
                module.students.remove(student)

        return redirect("itreporting:my_modules")

    return render(request, "itreporting/my_modules.html", {
        "modules": modules,
        "student": student,
    })

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

def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Create linked Student profile
            Student.objects.create(user=user)

            login(request, user)
            return redirect("module_list")
    else:
        form = StudentRegistrationForm()
        return render(request, "itreporting/register.html", {"form": form})

def email_signup(request):
    if request.method == "POST":
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            send_mail(
                subject="New Email Signup",
                message=f"New subscriber: {email}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )

            return redirect("signup_success")
    else:
        form = EmailSignupForm()

    return render(request, "newsletter/signup.html", {"form": form})

def about(request):
    return render(request, 'itreporting/about.html')