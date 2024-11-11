from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            
            # Send user registration data to Slack
            user_data = {
                "name": user.username,
                "email": user.email,
            }
            # send_slack_notification(user_data)

            messages.success(request, f"Account created for {user.username}!")
            return redirect('registration_success')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def registration_success(request):
    return render(request, 'registration_success.html')
