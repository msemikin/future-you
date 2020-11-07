from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.utils import translation


# Create your views here.
def index(request):
    template = "futureyou/pages/index.html"
    context = {}
    return render(request, template, context)


def report(request):
    template = "futureyou/pages/report.html"
    context = {}
    return render(request, template, context)


def goals(request):
    template = "futureyou/pages/goals.html"
    context = {}
    return render(request, template, context)


def transactions(request):
    template = "futureyou/pages/transactions.html"
    context = {}
    return render(request, template, context)

def image_upload(request):
    print(request)
    return redirect("home")

@login_required
def set_language(request: HttpRequest, lang: str) -> HttpResponse:
    """ Endpoint for setting language """
    available_langs = [x[0] for x in settings.LANGUAGES]
    response = HttpResponse(True)
    if lang in available_langs:
        translation.activate(language=lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
