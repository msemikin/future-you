from django.forms import ModelForm

from futureyou.models import ImageModel


class ImageModelForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = "__all__"