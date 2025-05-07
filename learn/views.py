
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TopicForm
from agents.crew import run_learning_path_crew 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from utils import load_data
from rest_framework.decorators import api_view
from .models import Topic, Module, Lesson, Resource, Exercise
from .forms import TopicForm
from utils.markdown_parser import parse_learning_path
import markdown
import json

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
        return render(request, "learn/learning_path.html", {"error": "No learning path found."})

    full_markdown = (
        f"# {result.get('topic_title', '')}\n\n"
        f"{result.get('topic_description', '')}\n\n"
        f"{result.get('topic_content', '')}\n\n"
        f"{result.get('modules_data', '')}"
    )
    
    topic_content_html = markdown.markdown(result.get("topic_content", ""))
    modules_data_html = markdown.markdown(result.get("modules_data", ""))
    
    parsed_data = parse_learning_path(full_markdown, dry_run=True)
    
    request.session['parsed_learning_path'] = parsed_data
    
    return render(request, "learn/learning_path.html", {
        "topic": result.get("topic_title", ""),
        "description": result.get("topic_description", ""),
        "topic_content_html": topic_content_html,
        "modules_data_html": modules_data_html,
        "parsed_data": json.dumps(parsed_data, indent=2),  
    })

@login_required
def edit_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learn:dashboard')
    else:
        form = TopicForm(instance=topic)
    return render(request, 'learn/edit_topic.html', {'form': form, 'topic': topic})

def delete_topic_confirm(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'learn/delete_topic_confirm.html', {'topic': topic})

@require_POST
def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    topic.delete()
    return redirect('learn:dashboard')

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

@login_required
def save_learning_path(request):
    if not request.session.get('parsed_learning_path'):
        messages.error(request, "No learning path data found to save")
        return redirect('learn:learning_path_view')
    
    try:
        parsed_data = request.session['parsed_learning_path']
        user = request.user
        
        topic = Topic.objects.create(
            title=parsed_data['topic']['title'],
            description=parsed_data['topic']['description'],
            content=json.dumps(parsed_data),
            user=user
        )
        
        for module_idx, module_data in enumerate(parsed_data['modules'], start=1):
            module = Module.objects.create(
                title=module_data['title'],
                topic=topic,
                order=module_idx,
                summary='', 
                content=''
            )
            

            for lesson_idx, lesson_data in enumerate(module_data['lessons'], start=1):
                lesson = Lesson.objects.create(
                    title=lesson_data['title'],
                    content="\n".join(lesson_data['key_concepts']),
                    module=module,
                    order=lesson_idx
                )
                

                for exercise_text in lesson_data['exercises']:
                    Exercise.objects.create(
                        prompt=exercise_text,
                        solution='', 
                        lesson=lesson
                    )
                

                for resource_text in lesson_data['resources']:

                    parts = [p.strip() for p in resource_text.split(':') if p.strip()]
                    if len(parts) >= 2:
                        resource_type = parts[0]
                        rest = ':'.join(parts[1:])
                        

                        url = ''
                        if 'http' in rest:
                            url = rest[rest.find('http'):].split()[0]
                            rest = rest[:rest.find('http')].strip()
                        

                        source = ''
                        if ' by ' in rest.lower():
                            rest, source = rest.rsplit(' by ', 1)
                        
                        Resource.objects.create(
                            title=f"{resource_type}: {rest.strip()}",
                            url=url,
                            source=source.strip(),
                            module=module
                        )
        
        del request.session['parsed_learning_path']
        if 'crew_result' in request.session:
            del request.session['crew_result']
        
        messages.success(request, f"Successfully saved learning path: {topic.title}")
        return redirect('learn:topic_detail', topic_id=topic.pk)
    
    except Exception as e:
        messages.error(request, f"Error saving learning path: {str(e)}")
        return redirect('learn:learning_path_view')

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