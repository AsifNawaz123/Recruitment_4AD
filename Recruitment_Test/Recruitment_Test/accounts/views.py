from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from Condidate.models import Candidate,CandidateDocument
from  accounts.models import UserProfile
from django.http import HttpResponse

@csrf_exempt
def userlogin(request):
     if request.method=='POST':
         #.get('is_private', False)
         name=request.POST.get('name',False)
         password=request.POST.get('pass',False)
         if(name!='asif' and password!='mcapgcet'):

             return HttpResponse("User is Authenticate to login,Please Enter the correct username and password")
         else:

            candi = UserProfile.objects.all()
            context = {'candidate': candi}
            return render(request, 'Condidate/details.html', context)
     else:
         return render_to_response('accounts/login.html')

