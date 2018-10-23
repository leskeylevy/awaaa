from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .forms import ProjectForm, ProfileForm, Rates
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import *
from .permissions import IsAdminOrReadOnly


# Create your views here.
@login_required
def index(request):
    projects = Projects.get_all()
    pro = ProjectForm()
    review = Rates()

    return render(request, 'index.html', locals())


# def rate(request,rate_id):
#     current_ user = request.user
#     project = get_object_or_404(Projects,pk=rate_id)
#     if request.method == 'POST':
#         review = Rates(request.POST)
#         if review.is_valid():
#             design = review.cleaned_data['design']
#             content = review.cleaned_data['content']
#             usability = review.cleaned_data['usability']
#             creativity = review.cleaned_data['creativity']
#             votes = Ratings(design=design, usability=usability,
#                             content=content, creativity=creativity,
#                             user=request.user, project=project)
#             votes.save()
#             return redirect('/')
#     return render(request, 'index.html', locals())

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(user=user)
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your awaaa account.'
            message = render_to_string('ActivationEmail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
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
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            'Thank you for your email confirmation. Now you can' '<a href="/accounts/login"> login </a>your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def project(request):
    if request.method == 'POST':
        pro = ProjectForm(request.POST, request.FILES)
        if pro.is_valid():
            projo = pro.save(commit=False)
            projo.user = request.user
            projo.save()
            return render(request, 'index.html', {'pro': pro})
        return redirect('index')


@login_required
def profile(request, profile_id):
    view_profile = Profile.objects.get(user_id=profile_id)
    projects = Projects.objects.filter(profile=profile_id)
    return render(request, 'profile.html', locals())


def search_results(request):
    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Projects.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


@login_required
def me_profile(request):
    current_user = request.user
    pro = ProjectForm()
    form = ProfileForm()
    profile = Profile.objects.all().filter(user=current_user.id)
    projs = Projects.objects.filter(user=current_user.id)
    if request.method == 'POST':
        pro = ProjectForm(request.POST, request.FILES)
        form = ProfileForm(request.POST, request.FILES, instance=current_user.profile)
        if pro.is_valid():
            prjct = pro.save(commit=False)
            prjct.user = current_user
            prjct.save()
            print('valid')
            return render(request, 'profile.html', locals())
        if form.is_valid():
            print('valid')
            prf = form.save(commit=False)
            prf.user = current_user
            prf.save()
            print(prf)
        return render(request, 'profile.html', locals())
    return render(request, 'profile.html', locals())


def rate(request, ratings_id):
    title = 'awards'
    current_user = request.user
    prjct = get_object_or_404(Projects, pk=ratings_id)
    if request.method == 'POST':
        review = Rates(request.POST)
        if review.is_valid():
            design = review.cleaned_data['design']
            content = review.cleaned_data['content']
            usability = review.cleaned_data['usability']
            creativity = review.cleaned_data['creativity']
            votes = Ratings(design=design, usability=usability,
                            content=content, creativity=creativity,
                            user=request.user, project=prjct)
            votes.save()
            return redirect('/')
    return render(request, 'index.html', locals())


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profs = Profile.objects.all()
        serializers = ProfileSerializer(all_profs, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_merch(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ProfileSerializer(merch)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ProfileSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectList(APIView):
    def get(self, request, format=None):
        all_merch = Projects.objects.all()
        serializers = ProjectsSerializer(all_merch, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectsSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_merch(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ProjectSerializer(merch)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = ProfileSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
