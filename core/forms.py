
from django import forms

from core.models import Drawing


class DrawingForm(forms.ModelForm):

    class Meta:
        model = Drawing
        fields = ("title",)
