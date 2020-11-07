from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.utils import translation

from futureyou.forms import ImageModelForm, GoalFormSet

from PIL import Image
import base64
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt

from transactions.TransactionsModel import TransactionsModel

t_model = TransactionsModel()


# Create your views here.
def index(request):
    template = "futureyou/pages/index.html"
    context = {}
    if request.method == 'POST' and request.FILES['image']:
        form = ImageModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            request.session['upload_image_id'] = new_image.pk
            request.session['upload_image_path'] = new_image.image.path
            request.session['upload_image_url'] = new_image.image.url
            s = new_image.image.url.split("/")
            v = "/".join(s[2:])
            request.session['upload_image_file_name'] = v
            context["uploaded_file_url"] = v
            context["form"] = form
    context["path"] = settings.MEDIA_ROOT
    return render(request, template, context)


def report_image_encoded():
    # Photo as PIL image
    photo = Image.new('RGB', (200, 200), (255,0,0))
    # Encode magic
    buffered = BytesIO()
    photo.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


def report(request):
    template = "futureyou/pages/report.html"
    context = {}

    # ----------------------------------
    # TODO: This context comes from some other place
    # ----------------------------------
    user_name = "Test user"
    user_iban = t_model.get_random_bank_account()
    current_date = datetime.now().date()
    buckets = {
        'Housing': 100,
        'Clothing': 50,
        'Education': 200,
        'Food': 300
    }
    # Score 0 to 1
    goals = [
        {'Retire': 1.0, 'description': 'Keep my lifestyle when I retire'},
        {'Savings': 0.7, 'description': 'Be prepared for surprises'}
    ]
    # ----------------------------------

    # Report data
    report_data = t_model.get_report_data(user_iban, buckets, goals, current_date)
    
    # Week plot
    week_plot = report_data['week_plot']
    fig = plt.Figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    ax = week_plot.plot.bar(ax=ax)
    buffered = BytesIO()
    fig.savefig(buffered, format='png', dpi=100)
    context['week_plot'] = base64.b64encode(buffered.getvalue()).decode('utf-8')

    context['photo'] = report_image_encoded()
    return render(request, template, context)


def goals(request):
    template = "futureyou/pages/goals.html"
    context = {}
    context["goals"] = request.session["goals"] if "goals" in request.session else []
    initial_data = [
        {
            "goal": "Your first goal",
            "priority": 1,
        },
        {
            "goal": "Your second goal",
            "priority": 2,
        },
        {
            "goal": "Your third goal",
            "priority": 3,
        },
        {
            "goal": "Your fourth goal",
            "priority": 4,
        },
        {
            "goal": "Your fifth goal",
            "priority": 5,
        }
    ]
    initial_data = request.session["forms"] if "forms" in request.session else initial_data
    forms = GoalFormSet(initial=initial_data)
    if (request.method == "POST"):
        forms = GoalFormSet(request.POST)
        # print formset data if it is valid
        if forms.is_valid():
            request.session["forms"] = forms.cleaned_data
    context["forms"] = forms
    return render(request, template, context)


def transactions(request):
    template = "futureyou/pages/transactions.html"
    context = {}
    return render(request, template, context)


def image_upload(request):
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
