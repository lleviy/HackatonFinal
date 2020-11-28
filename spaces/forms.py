from django import forms

from .models import Space


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Файл')
    is_on_main_map = forms.BooleanField(label='Загрузить данные на главную карту')


class SpaceForm(forms.ModelForm):
    file = forms.FileField(label='Файл', help_text='только файлы в формате .xls', required=False)

    class Meta:
        model = Space
        fields = ('name', )
        labels = {
            'name': 'Название',
        }