from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile


# Below function is used to get the object of currently logged-in user and use that to get the user profile
@login_required()
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    return JsonResponse({
        "username": user_profile.user.username,
        "message": "User logged in"
    })


# Below function takes data from request to register a new user profile
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_super_user = request.POST.get('isSuperUser')
        print(is_super_user)

        # Proceed if the entered password matches with the conform password
        if password == password2:
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already exists"})
            elif User.objects.filter(username=username).exists():
                return JsonResponse({"message": "Username already exists"})
            else:
                if is_super_user == 'true':
                    print("Creating superuser")
                    user = User.objects.create_superuser(username=username, email=email, password=password)
                else:
                    print("Creating normal user")
                    user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in after registering
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, is_super_user=user_model.is_superuser)
                new_profile.save()

                return JsonResponse({
                    "username": user_model.username,
                    "email": user_model.email,
                    "isSuperUser": user_model.is_superuser,
                    "message": "User successfully registered."
                })
        else:
            return JsonResponse({
                "username": username,
                "email": email,
                "message": "Passwords do not match. Please try again."
            })


# Below function is used to authenticate a current user profile
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        # If the credentials match from the auth DB, then login
        if user is not None:
            auth.login(request, user)
            return JsonResponse({
                "username": username,
                "message": "Signin successful"
            })
        else:
            return JsonResponse({
                "message": "Invalid credentials"
            })

    else:
        return JsonResponse({
            "message": "An error occurred."
        })


# Below function is used to logout the current user
@login_required()
def logout(request):
    auth.logout(request)
    return JsonResponse({
        "message": "Logout successful"
    })
