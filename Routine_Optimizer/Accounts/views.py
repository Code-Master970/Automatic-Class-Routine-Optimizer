from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Faculty
from django.contrib.auth.decorators import login_required


# Create your views here.


#functions for page viewing
@login_required(login_url='/signup_or_login/')
def Dashboard(request):
    return render(request,'Dashboard/faculty.html')

def Personal_details(request):
    return render(request, 'Dashboard/details.html')

def Password(request):
    return render(request, 'Dashboard/password.html')

def Signup(request):
    return render(request, 'Signup/index.html')




# functions for register,login and logout feature.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number'] 
        college_id = request.POST['college_id']
        subject = request.POST['subject']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        photo = request.FILES.get('photo')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('/signup_or_login/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('/signup_or_login/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('/signup_or_login/')
        
        if Faculty.objects.filter(college_id=college_id).exists():
            messages.error(request, "This Faculty ID is already exists!")
            return redirect('/signup_or_login/')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        # Create faculty profile
        faculty = Faculty.objects.create(
            user=user,
            email=email,
            phone_number=phone_number,
            college_id=college_id,
            subject=subject,
            photo=photo
        )
        faculty.save()

        messages.success(request, "Account created successfully! You can now login.")
        return redirect('/dashboard/')

    return render(request, '/signup_or_login/')


def user_login(request):
    if request.method == 'POST':
        college_id = request.POST['college_id']
        password = request.POST['password']

        try:
            faculty = Faculty.objects.get(college_id=college_id)
            user = authenticate(request, username=faculty.user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                messages.error(request, "Invalid password")
        except Faculty.DoesNotExist:
            messages.error(request, "No faculty found with this College ID")

    return render(request, 'Signup/index.html')



def logout_user(request):
    logout(request)
    messages.success(request, "Logged out Successfull!")
    return redirect("/")



@login_required(login_url='/signup_or_login/')
def Personal_details_update(request):
    user = request.user
    faculty = request.user.faculty  # Ensure OneToOne relation

    if request.method == 'POST':
        # Get updated data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('subject')
        college_id = request.POST.get('college_id')

        # Prevent accidental empty updates
        if username:
            user.username = username
        if email:
            user.email = email
        if phone_number:
            faculty.phone_number = phone_number
        if subject:
            faculty.subject = subject
        if college_id:
            faculty.college_id = college_id

        # Check if a new photo was uploaded
        if 'photo' in request.FILES:
            faculty.photo = request.FILES['photo']

        # Debugging prints to check values
        print("Username:", user.username)
        print("Email:", user.email)
        print("Phone Number:", faculty.phone_number)
        print("Subject:", faculty.subject)
        print("College ID:", faculty.college_id)

        user.save()
        faculty.save()

        messages.success(request, "Personal details updated successfully!")
        return redirect('/dashboard/personal_details/')

    return render(request, 'Dashboard/details.html', {'user': user})




@login_required(login_url='/signup_or_login/')
def Update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Check if current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('/dashboard/password/')

        # Check if new password matches confirm password
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('/dashboard/password/')

        # Update password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return redirect('/dashboard/')

    return render(request, 'Dashboard/password.html')


