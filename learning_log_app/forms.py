#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# Time    : 2025/6/15 16:52
# File    : forms.py
# Software: PyCharm
from django import forms

from learning_log_app.models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text']
        labels = {'title': '标题', 'text': '内容'}
        widgets = {
            'title': forms.Textarea(attrs={'placeholder': '可选标题'}),
            'text': forms.Textarea(attrs={'placeholder': '在这里输入内容'})
        }

class CustomUserCreationForm(forms.ModelForm):
    pass
class UserEditForm(forms.ModelForm):
    pass
