from django import forms
from .models import WorkingTimeModel

class WorkingForm(forms.ModelForm):
    class Meta:
        model = WorkingTimeModel
        fields = ("start", "finish")
        labels = {
            "start": "開始時刻",
            "finish": "終了時刻"
        }