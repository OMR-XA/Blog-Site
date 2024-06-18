from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from Reg.nudedetector import check_image_safety, save_temp_image
import re
import os
import uuid


def signup(request):
    if request.method == "POST":
        if "SignUp" in request.POST:
            # Get form data
            name1 = request.POST.get("first_name")
            name2 = request.POST.get("last_name")
            email = request.POST.get("sign_email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            birthday = request.POST.get("bd")
            username = request.POST.get("username")
            pic = request.FILES.get("image")

            # Validate email
            email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not re.match(email_regex, email):
                # messages.error(request, "Enter a valid email")
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Invalid email, try another one"})
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                # messages.error(request, "Email already exists")
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Email already exists"})

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                # messages.error(request, "Username already exists, try another one")
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Username already exists"})
            # Password strength
            if len(password) < 8 or not any(char in "_@#-!.&$" for char in password):
                # messages.error(request, "Password too weak, use at least one special character and a minimum of 8 characters")
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Password too weak, use at least one special character and a minimum of 8 characters"})

            # Password match
            if password != password2:
                messages.error(request, "Passwords do not match")
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Passwords do not match"})

            # Save the uploaded image temporarily
            if pic:
                temp_image_path = save_temp_image(pic)
                pic_result = check_image_safety(temp_image_path)
                os.remove(temp_image_path)  # Delete the temp file after checking
                if pic_result == "Not Safe":
                    # messages.error(request, "Image is not safe")
                    return render(request, 'Signup.html', {'data': request.POST,"message" : "Picture not safe"})

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name1,
                last_name=name2
            )
            user.save()

            # Create user profile
            userprofile = UserProfile(
                user=user,
                birthday=birthday,
                pic=pic,
                username=username,
            )
            userprofile.save()

            messages.success(request, "Account created successfully! ")
            login(request, user)
            return redirect('/scroll')  # Redirect to login page after successful signup

        if "LogIn" in request.POST:
            email = request.POST.get("log_email")
            password = request.POST.get("log_password")

            # Fetch the user by email
            try:
                user_profile = UserProfile.objects.get(user__email=email)
                user = authenticate(request, username=user_profile.user.username, password=password)
                if user is not None:
                    messages.success(request, "Logged in successfully")
                    login(request, user)
                    return redirect("/scroll")
                else:
                    return render(request, 'Signup.html', {'data': request.POST,"message" : "Wrong email or password"})
            except UserProfile.DoesNotExist:
                return render(request, 'Signup.html', {'data': request.POST,"message" : "Wrong email or password"})

    return render(request, 'Signup.html')
