from django.shortcuts import render, get_object_or_404, redirect
from .forms import TopicForm
from agents.crew import run_learning_path_crew 
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    topics = Topic.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'learn/dashboard.html', {'topics': topics})

def topic_generate(request):
    if request.method == 'POST':
        # Placeholder until AI integration
        topic = Topic.objects.create(user=request.user, title="Placeholder Topic", summary="AI-generated summary")
        return redirect('topic_detail', topic_id=topic.id)
    return render(request, 'learn/topic_generate.html')

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    return render(request, 'learn/topic_detail.html', {'topic': topic})

def module_detail(request, topic_id, module_id):
    module = get_object_or_404(Module, id=module_id, topic__id=topic_id, topic__user=request.user)
    return render(request, 'learn/module_detail.html', {'module': module})

def lesson_detail(request, topic_id, module_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__id=module_id, module__topic__id=topic_id, module__topic__user=request.user)
    return render(request, 'learn/lesson_detail.html', {'lesson': lesson})