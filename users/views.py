from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile, Hackathon, Submission
from django.core import serializers


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


# Below function is used to post a new hackathon. Only superusers are allowed to post a hackathon.
# If the logged-in user is a superuser then he is allowed to post a hackathon, else not.
@login_required()
def post_hackathon(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            user = request.user.username
            title = request.POST.get('title')
            description = request.POST.get('description')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            if Hackathon.objects.filter(title=title).exists():
                return HttpResponse("Hackathon with this name already exists. Choose another name.")
            else:
                new_hackathon = Hackathon.objects.create(
                    user=user, title=title, description=description,
                    start_time=start_time, end_time=end_time)

                new_hackathon.save()
                return JsonResponse({
                    "id": new_hackathon.id,
                    "name": new_hackathon.title,
                    "message": "Hackathon posted successfully."
                })
        else:
            return HttpResponse('Some error occurred.')
    else:
        return HttpResponse('You have to be a superuser to post a hackathon.')


# Get the JSON response containing all the posted hackathons.
def get_hackathons(request):
    all_hackathons = Hackathon.objects.all()
    data = serializers.serialize('json', all_hackathons)
    return JsonResponse(data, safe=False)


# Below function is used to registering a user for a hackathon.
# The user provides the title of the hackathon that he wants to register in.
# User can only be registered into one hackathon at a time.
@login_required()
def register_for_hackathon(request):
    if request.method == 'POST':
        hackathon_title = request.POST.get('hackathon_title')
        user = request.user.username

        if Profile.objects.get(id_user=request.user.id).registered_hackathon is not '.':
            return JsonResponse({
                "hackathon_title": hackathon_title,
                "user": user,
                "message": "You are already registered."
            })
        else:
            if Hackathon.objects.filter(title=hackathon_title).exists():
                cur_user = Profile.objects.get(id_user=request.user.id)
                cur_user.registered_hackathon = hackathon_title
                cur_user.save()
                return JsonResponse({
                    "username": cur_user.user.username,
                    "registered_hackathon": cur_user.registered_hackathon,
                    "message": "Registered successfully."
                })
            else:
                return HttpResponse('The hackathon of the provided title does not exist.')

    else:
        return HttpResponse('Some error occurred.')


# Function to get all submissions to a particular hackathon
def get_all_submissions(request):
    all_submissions = Submission.objects.all()
    data = serializers.serialize('json', all_submissions)
    return JsonResponse(data, safe=False)


# Below function is used to make a submission to the registered hackathon by the user.
@login_required()
def make_submission(request):
    if request.method == 'POST':
        submission_name = request.POST.get('submission_name')
        summary = request.POST.get('summary')
        hackathon_title = request.POST.get('hackathon_title')
        github_link = request.POST.get('github_link')

        if Profile.objects.get(id_user=request.user.id).registered_hackathon != hackathon_title:
            return HttpResponse('Yor are not registered for this hackathon.')
        elif Profile.objects.get(id_user=request.user.id).registered_hackathon == hackathon_title:
            return JsonResponse({
                "username": request.user.username,
                "hackathon_title": hackathon_title,
                "message": "You have already submitted your submission."
            })
        else:
            new_submission = Submission.objects.create(
                submission_name=submission_name,
                summary=summary,
                hackathon_title=hackathon_title,
                github_link=github_link
            )

            new_submission.save()
            return JsonResponse({
                "id": new_submission.id,
                "submission_name": new_submission.submission_name,
                "hackathon_title": new_submission.hackathon_title,
                "message": "Submission uploaded successfully."
            })

    else:
        return HttpResponse("An error occurred.")

