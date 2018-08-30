from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from accounts.models import UserProfile
from .forms import UserApplyStep1Form, UserApplyStep2Form
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Candidate, CandidateDocument
from django.http import HttpResponse


@csrf_exempt
def home(request):
    if request.method=='POST':
        if request.POST.get("Apply"):
            return redirect('candidates/apply/')
        elif request.POST.get("Login"):
            return redirect('login')

    else:
        return render_to_response('Condidate/Home.html')


def apply(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if not key and request.method == 'POST':

        form = UserApplyStep1Form(request.POST)

        if form.is_valid():
            data = form.data
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            citizenship = data['citizenship']
            skype_id = data['skype_id']
            timezone = data['timezone']

            user, created = User.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email
            )

            if not created:
                messages.add_message(request, messages.ERROR,
                                     email + ' has already been registered.')
            else:
                userprofile = UserProfile(
                    first_name=first_name,
                    last_name=last_name,
                    user=user,
                    timezone=timezone,
                    citizenship=citizenship,
                    skype_id=skype_id,
                    user_type='Candidate'
                )

                userprofile.save()

                key = user.userprofile.generate_token()

                return HttpResponseRedirect(
                    reverse('candidate_apply') + '?key=' + key)


    elif not key and request.method == 'GET':
        form = UserApplyStep1Form()

    elif key and user and request.method == 'POST':

        form = UserApplyStep2Form(request.POST, request.FILES)

        if form.is_valid():
            files = form.files
            data = form.data

            try:
                candidate = user.candidate
                candidate.birth_year = data['birth_year']
                candidate.gender = data['gender']
                candidate.education = data['education']
                candidate.education_major = data['education_major']
                candidate.image = files['image']
                candidate.save()
            except Candidate.DoesNotExist:
                candidate = Candidate.objects.create(user=user,
                                                     birth_year=data['birth_year'],
                                                     gender=data['gender'],
                                                     education=data['education'],
                                                     education_major=data['education_major'],
                                                     image=files['image']
                                                     )
            CandidateDocument.objects.create(
                candidate=candidate,
                document=files['resume'],
                document_type='Resume'
            )

            messages.add_message(request, messages.SUCCESS,
                                 'Form submitted successfully.')

            return HttpResponseRedirect(
                reverse('candidate_apply_success') + '?key=' + key)

    elif key and user and request.method == 'GET':
        form = UserApplyStep2Form()

    else:
        messages.add_message(request, messages.ERROR,
                             'A valid application key is required to submit documents. ' +
                             'Please contact the administrator.')
        form = None

    return render(request, 'Condidate/apply.html', {'form': form})


def apply_success(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if not key or not user:
        messages.add_message(request, messages.ERROR,
                             'A valid application key is required to view this page.')


    return render(request, 'Condidate/apply.html',
                  {'success': 'success'
                   })

@csrf_exempt
def detail(request,id_num):

    if request.method=='POST':
        if request.POST.get("Accept"):
            candi = UserProfile.objects.all()
            abc={'success': 'success', 'candi': candi, 'id_no': id_num}
            print(abc)
            return render(request, 'Condidate/details.html',
                          {'success': 'success','candi': candi,'id_no':id_num
                           })
            #return HttpResponse('Congrations Application Got Accepted')
        elif request.POST.get("Reject"):

            UserProfile.objects.filter(id=id_num).delete()
            candi = UserProfile.objects.all()
            context = {'candidate': candi}
            return render(request, 'Condidate/details.html', context)
    else:
        User_list = UserProfile.objects.filter(id=id_num)
        Candidate_list=Candidate.objects.filter(id=id_num)

        print(Candidate_list)
        context = {'details': User_list}
        return render(request, 'Condidate/list_details.html', context)
    #Candidate.objects.get(user=user)
    #return HttpResponse("You're voting on question %s." % id_num)