from django import forms
from .models import Topic, Module, Lesson, Exercise, Resource

class TopicForm(forms.Form):
    topic = forms.CharField(label="What do you want to learn?", max_length=200)

from django import forms

class TopicTitleForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'summary', 'content', 'topic', 'order']

# Lesson Form
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'module', 'order']

# Exercise Form
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['prompt', 'solution', 'lesson']

# Resource Form
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'url', 'source', 'module']