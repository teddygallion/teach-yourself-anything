from django.shortcuts import render, get_object_or_404, redirect
from .forms import TopicForm
from agents.crew import run_learning_path_crew 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseBadRequest
from utils import load_data
from rest_framework.decorators import api_view
from .models import Topic, Module, Lesson, Resource
from .forms import TopicForm
from utils.markdown_parser import parse_roadmap
import markdown

def home(request):
    return render(request, 'learn/home.html')

@login_required
def dashboard(request):
    topics = Topic.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'learn/dashboard.html', {'topics': topics})

def topic_generate(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        result = run_learning_path_crew(topic)

        request.session["crew_result"] = result  

        return redirect("learn:learning_path_view") 

    return render(request, "learn/topic_generate.html")
@login_required
def learning_path_view(request):
    result = request.session.get("crew_result")
    if not result:
        return render(request, "learn/learning_path.html", {})

    topic_title = result.get("topic_title")
    topic_description = result.get("topic_description")
    modules_data = result.get("modules", [])

    # Save topic
    topic = Topic.objects.create(
        title=topic_title,
        description=topic_description,
        user=request.user
    )

    for mod in modules_data:
        module = Module.objects.create(
            topic=topic,
            title=mod.get("title", ""),
            summary=mod.get("summary", "")
        )

        for les in mod.get("lessons", []):
            Lesson.objects.create(
                module=module,
                title=les.get("title", ""),
                content=les.get("content", ""),
                exercises=les.get("exercises", []),
                resources=les.get("resources", [])
            )

    # Optional: redirect to a topic detail view
    return render(request, "learn/learning_path.html", {
        "topic": topic_title,
        "modules": modules_data
    })

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    modules = topic.modules.all()  
    return render(request, 'learn/topic_detail.html', {'topic': topic, 'modules': modules})

def module_detail(request, topic_id, module_id):
    module = get_object_or_404(Module, id=module_id, topic__id=topic_id, topic__user=request.user)
    return render(request, 'learn/module_detail.html', {'module': module})

def lesson_detail(request, topic_id, module_id, lesson_id):

    lesson = get_object_or_404(Lesson, id=lesson_id, module__id=module_id, module__topic__id=topic_id, module__topic__user=request.user)
    
    
    resources = Resource.objects.filter(module=lesson.module)

    
    return render(request, 'learn/lesson_detail.html', {'lesson': lesson, 'resources': resources})

@api_view(['POST'])

def load_topic_data(request):
    try:
       
        data = request.data

       
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

      
        topic_title = data.get("topic_title")
        topic_description = data.get("topic_description")
        topic_content = data.get("topic_content")
        modules_data = data.get("modules_data")

        if not all([topic_title, topic_description, topic_content, modules_data]):
            return Response({"error": "Missing required data"}, status=status.HTTP_400_BAD_REQUEST)


        load_data(user, topic_title, topic_description, topic_content, modules_data)

        return Response({"message": "Data loaded successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:

        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)