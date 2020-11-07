from django.forms import ModelForm, formset_factory
from django import forms

from futureyou.models import ImageModel


class ImageModelForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = "__all__"


class GoalForm(forms.Form):
    goal = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    priority = forms.ChoiceField(choices=[(1, "Highest"), (2, "High"), (3, "Medium"), (4, "Low"), (5, "Lowest")],
                                 widget=forms.Select(attrs={"class": "form-control"}))
    comment = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 3,
        "placeholder": "What is the your aim for the goal? Why it is important for you?"
    }), required=False)


GoalFormSet = formset_factory(GoalForm, extra=0)

class BudgetForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    id = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    amount =  forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))


BudgetFormSet = formset_factory(BudgetForm, extra=0)