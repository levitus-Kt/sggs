from django import forms
from .models import LessonQuantity, Holidays, UploadFile
from django.forms import ModelForm


class UploadFileForm(ModelForm):
    file_pre = forms.FileField(allow_empty_file=False, required=True, label="Звонок за 3 минуты")
    file_in = forms.FileField(allow_empty_file=False, required=True, label="Звонок на урок")
    file_out = forms.FileField(allow_empty_file=False, required=True, label="Звонок с урока")
    class Meta:
        model = UploadFile
        fields = ['title']

class HolidaysForm(ModelForm):

    class Meta:
        model = Holidays
        fields = ['content']

    def clean(self):
        cleaned_data = super().clean()
    
class QuantityForm(ModelForm):

    class Meta:
        model = LessonQuantity
        fields = ['num']
