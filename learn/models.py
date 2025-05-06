from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)  
    topic = models.ForeignKey(Topic, related_name="modules", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

class Exercise(models.Model):
    prompt = models.TextField()
    solution = models.TextField(blank=True)
    lesson = models.ForeignKey(Lesson, related_name="exercises", on_delete=models.CASCADE)

    def __str__(self):
        return self.prompt[:50] + "..."

class Resource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    source = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, related_name="resources", on_delete=models.CASCADE)

    def __str__(self):
        return self.title