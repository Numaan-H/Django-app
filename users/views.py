from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm, EmailSignupForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required  

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data["email"]],
                fail_silently=False,
            )

            return render(
                request,
                "itreporting/contact.html",
                {
                    "form": ContactForm(),
                    "success": True
                }
            )
    else:
        form = ContactForm()

    return render(request, "itreporting/contact.html", {"form": form})
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, 'Your account has been successfully updated!')
        return redirect('profile')
    else:     
        u_form = UserUpdateForm(instance = request.user) 
        p_form = ProfileUpdateForm(instance = request.user.profile) 

    context = {'u_form': u_form, 'p_form': p_form, 'title': 'Student Profile'} 
    return render(request, 'users/profile.html', context) 
 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Now you can login!') 
            return redirect('login') 
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})

@login_required 
def profile(request):

    return render(request, 'users/profile.html', {'title': 'Student Profile'})