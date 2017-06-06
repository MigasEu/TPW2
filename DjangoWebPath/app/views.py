"""
Definition of views.
"""

from django.shortcuts import render
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.http import HttpRequest
from app.forms import BootstrapRegistrationForm
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse,HttpResponseRedirect
from datetime import datetime
from app.models import Story, Piece, DecisionPiece, ChoicePiece
from django.http import Http404
from django.shortcuts import get_object_or_404
from model_utils.managers import InheritanceManager
from django.core.exceptions import ObjectDoesNotExist
from app.serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import json
from django.db import transaction


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    allStories = Story.objects.all()
    myStories = None
    if request.user.is_authenticated():
        myStories = Story.objects.filter(creator=request.user)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'allStories': allStories,
            'myStories': myStories,
        }
    )

def playStory(request, storyId):
    assert isinstance(request, HttpRequest)
    story = get_object_or_404(Story, pk=storyId)
    firstPieceId = Piece.objects.filter(story=storyId).first()
    return render(
        request,
        'app/playStory.html',
        {
            'title':'Play '+story.title,
            'year':datetime.now().year,
            'story':story,
            'firstPiece':firstPieceId.pk
        }
    )

def getPiece(request, storyId, pieceId):
    assert isinstance(request, HttpRequest)
    try:
        piece = Piece.objects.get_subclass(story=Story.objects.get(pk=storyId), pId=pieceId)
    except ObjectDoesNotExist:
        raise Http404("No piece matches the given query.")

    choices = None
    if isinstance(piece, DecisionPiece):
        choices = ChoicePiece.objects.filter(decision=piece.pk)

    return render(
        request,
        'app/piece.html',
        {
            'title':'Piece '+str(piece.pk),
            'year':datetime.now().year,
            'piece':piece,
            'choices':choices
        }
    )

@login_required
def createStory(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/createStory.html',
        {
            'title':'Create Story',
            'year':datetime.now().year
        }
    )

@login_required
@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((permissions.AllowAny,))
def postStory(request, format=None):
    storyJ = json.loads(json.dumps(request.data))
    print(storyJ)
    with transaction.atomic():
        story = Story(title=storyJ["title"], creator=request.user)
        story.save()
        for p in storyJ["pieces"]:
            if p == None:
                continue

            pType = p["type"]
            del p["type"]
            p["story"] = story.pk
            if pType == 0:
                piece = Piece()
                seriaP = PieceSerializer(piece, data=p)
                seriaP.is_valid(raise_exception=True)
                seriaP.save()
            elif pType == 1:
                piece = DecisionPiece()
                choices = p["choices"]
                del p["choices"]
                print(p)
                seriaD = DecisionSerializer(piece, data=p)
                seriaD.is_valid(raise_exception=True)
                seriaD.save()
                for c in choices:
                    print(c)
                    choice = ChoicePiece(story=story, decision=piece)
                    seriaC = ChoiceSerializer(choice, data=c)
                    seriaC.is_valid(raise_exception=True)
                    seriaC.save()
            elif pType == 2:
                piece = LosePiece()
                seriaP = LoseSerializer(piece, data=p)
                seriaP.is_valid(raise_exception=True)
                seriaP.save()
            elif pType == 3:
                piece = WinPiece()
                seriaP = WinSerializer(piece, data=p)
                seriaP.is_valid(raise_exception=True)
                seriaP.save()

    return HttpResponse(status=201)

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def registration(request, template_name='app/registration.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          registration_form=UserCreationForm,
          current_app=None, extra_context=None):

    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = registration_form(request.POST or None)
        if form.is_valid():
      
            form.save();

            return HttpResponseRedirect(redirect_to)
    else:
        form = registration_form(request.POST or None)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
