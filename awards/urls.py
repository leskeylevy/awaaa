from django.conf import settings
from django.conf.urls import url, include
from . import views
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns=[
    url('^$', views.index,name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/', views.me_profile,name='myprofile'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^projects',views.project,name='projo'),
    url(r'^search/', views.search_results, name='search_results'),
    url('^review/(\d+)$', views.rate, name='review'),
    url(r'^api/profile/$', views.ProfileList.as_view()),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'api/projects/merch-id/(?P<pk>[0-9]+)/$',views.ProjectDescription.as_view()),
    url(r'api/profile/merch-id/(?P<pk>[0-9]+)/$',views.ProfileDescription.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)