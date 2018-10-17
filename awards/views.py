from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Projects,Profile
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    projects = Projects.get_all()
    pro = ProjectForm()
    return render(request, 'index.html', {'pro':pro, 'projects':projects})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your awaaa account.'
            message = render_to_string('ActivationEmail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        login(request,user)
        return HttpResponse(
            'Thank you for your email confirmation. Now you can' '<a href="/accounts/login"> login </a>your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def project(request):
    if request.method == 'POST':
        pro=ProjectForm(request.POST,request.FILES)
        if pro.is_valid():
            projo = pro.save(commit=False)
            projo.user=request.user
            projo.save()
            return render(request, 'index.html', {'pro':pro})
        return redirect(request, 'index.html', {'pro':pro})


@login_required
def profile(request):
    pro = ProjectForm()
    return render(request,'profile.html', {"pro":pro})


def search_results(request):
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Projects.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects":searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request,'search.html', {"message":message})



