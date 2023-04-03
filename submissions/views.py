from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Submission
from users.models import Profile
from django.core import serializers


@login_required()
def index(request):
    cur_user = request.user.username
    return JsonResponse({
        "username": cur_user,
        "message": "You are in submissions portal."
    })


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


