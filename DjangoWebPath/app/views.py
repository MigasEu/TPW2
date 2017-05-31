"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.models import Story, Piece, DecisionPiece, ChoicePiece
from django.http import Http404
from django.shortcuts import get_object_or_404
from model_utils.managers import InheritanceManager
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def playStory(request, storyId):
    assert isinstance(request, HttpRequest)
    story = get_object_or_404(Story, pk=storyId)
    return render(
        request,
        'app/playStory.html',
        {
            'title':'Play '+story.title,
            'year':datetime.now().year,
            'story':story
        }
    )

def getPiece(request, storyId, pieceId):
    assert isinstance(request, HttpRequest)
    try:
        piece = Piece.objects.get_subclass(pk=pieceId)
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
