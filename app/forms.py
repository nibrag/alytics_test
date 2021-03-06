# coding: utf-8
from __future__ import absolute_import
import json
from django import forms
from .models import Data


class AddDataForm(forms.ModelForm):
    name = forms.CharField(max_length=129, label='Название данных')
    data = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'span8', 'placeholder': '[{"a": 1, "b": 1}, {"a": 2, "b": 3]'}),
        label='Данные')

    def clean_data(self):
        try:
            data = json.loads(self.cleaned_data['data'])
            if not isinstance(data, list):
                raise ValueError
        except (TypeError, ValueError):
            raise forms.ValidationError('Неверный json объект')
        return data

    class Meta:
        model = Data
        fields = ('name', 'data')
