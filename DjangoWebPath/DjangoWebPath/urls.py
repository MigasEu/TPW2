"""
Definition of urls for DjangoWebPath.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from django.views.generic import TemplateView

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^api/story$', app.views.postStory, name='rest_story_post'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^play/(?P<storyId>\d+)/$',
        app.views.playStory, name='playStory'),
    url(r'^play/(?P<storyId>\d+)/(?P<pieceId>\d+)/$',
        app.views.getPiece, name='getPiece'),
    url(r'^create$',
        app.views.createStory, name='createStory'),
    url(r'^template/createPiece$', TemplateView.as_view(template_name='app/createPiece.html')),
    url(r'^template/createEvent$', TemplateView.as_view(template_name='app/createEvent.html')),
    url(r'^template/createChoices$', TemplateView.as_view(template_name='app/createChoices.html')),
    url(r'^template/createChoice$', TemplateView.as_view(template_name='app/createChoice.html')),
    url(r'^template/createFinal$', TemplateView.as_view(template_name='app/createFinal.html')),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

     url(r'^register/$',
        app.views.registration,
        {
            'template_name': 'app/registration.html',
            'registration_form': app.forms.BootstrapRegistrationForm,
            'extra_context':
            {
                'title': 'Sign up',
                'year': datetime.now().year,
            }
        },
        name='registration'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


]
