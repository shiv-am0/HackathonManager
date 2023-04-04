import datetime
import pytz
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


# Function to get all submissions to a particular hackathon. Submissions can only be viewed by superusers.
# Submissions can be viewed from newest to oldest and vice versa by passing ASC/DESC in sort_by field.
@login_required()
def get_all_submissions(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            hackathon_title = request.POST.get('hackathon_title')
            sort_by = request.POST.get('sort_by')
            print(hackathon_title)
            all_submissions = Submission.objects.all()
            print(all_submissions)
            res = []

            if sort_by == 'ASC':
                all_submissions = all_submissions.order_by('submission_time')
            elif sort_by == 'DESC':
                all_submissions = all_submissions.order_by('-submission_time')
            else:
                return HttpResponse('Please enter a valid sort_by command, i.e. ASC/DESC')

            found = False
            for sub in all_submissions:
                if sub.hackathon_title == str(hackathon_title):
                    found = True
                    res.append(sub)

            if found is True:
                data = serializers.serialize('json', res)
                print(f'Data = {data}')
                return JsonResponse(data, safe=False)
            else:
                return HttpResponse("There are no submissions.")
        else:
            return HttpResponse("An error occurred.")
    else:
        return HttpResponse('You have to be a superuser to view the submissions.')


# Below function is used to make a submission to the registered hackathon by the user.
@login_required()
def make_submission(request):
    if request.method == 'POST':
        submission_name = request.POST.get('submission_name')
        summary = request.POST.get('summary')
        hackathon_title = request.POST.get('hackathon_title')
        github_link = request.POST.get('github_link')
        created_by = request.user.username

        if Profile.objects.get(id_user=request.user.id).registered_hackathon != hackathon_title:
            return HttpResponse('Yor are not registered for this hackathon.')
        elif Profile.objects.get(id_user=request.user.id).registered_hackathon == hackathon_title and \
                Submission.objects.filter(created_by=created_by).exists():
            return JsonResponse({
                "username": request.user.username,
                "created_by": created_by,
                "hackathon_title": hackathon_title,
                "message": "You have already submitted your submission."
            })
        else:
            new_submission = Submission.objects.create(
                submission_name=submission_name,
                summary=summary,
                hackathon_title=hackathon_title,
                github_link=github_link,
                created_by=created_by,
                submission_time=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
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


# Delete a submission based on its submission name and hackathon title.
@login_required()
def delete_submission(request):
    if request.method == 'POST':
        submission_name = request.POST.get('submission_name')
        hackathon_title = request.POST.get('hackathon_title')
        created_by = request.user.username

        if Submission.objects.filter(submission_name=submission_name, hackathon_title=hackathon_title,
                                     created_by=created_by).exists():
            my_submission = Submission.objects.get(submission_name=submission_name, hackathon_title=hackathon_title,
                                                   created_by=created_by)

            my_submission.delete()

            return JsonResponse({
                "submission_name": my_submission.submission_name,
                "hackathon_title": my_submission.hackathon_title,
                "created_by": my_submission.created_by,
                "message": "Submission deleted successfully."
            })
        else:
            return HttpResponse("This submission can not be deleted.")
    else:
        return HttpResponse("An error occurred.")
