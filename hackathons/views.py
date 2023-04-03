from django.contrib.auth.decorators import login_required
from django.core import serializers
from users.models import Profile
from django.http import HttpResponse, JsonResponse
from .models import Hackathon


# Root Function
@login_required()
def index(request):
    cur_user = request.user.username
    return JsonResponse({
        "username": cur_user,
        "message": "You are in hackathons portal."
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
@login_required()
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
