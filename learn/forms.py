from django import forms

class TopicForm(forms.Form):
    topic = forms.CharField(label="What do you want to learn?", max_length=200)
