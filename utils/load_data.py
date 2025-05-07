from learn.models import Topic, Module, Lesson, Exercise, Resource

def load_data(user, topic_title, topic_description, topic_content, modules_data):

    topic = Topic.objects.create(
        title=topic_title,
        description=topic_description,  
        content=topic_content, 
        user=user
    )

    for i, mod_data in enumerate(modules_data):
        
        module = Module.objects.create(
            title=mod_data["title"],
            summary=mod_data.get("summary", ""),
            content=mod_data.get("content", ""),  
            topic=topic,
            order=i
        )


        for resource_data in mod_data.get("resources", []):
            Resource.objects.create(
                title=resource_data["title"],
                url=resource_data["url"],
                source=resource_data.get("source", ""),
                module=module
            )

        for j, les_data in enumerate(mod_data["lessons"]):
            lesson = Lesson.objects.create(
                title=les_data["title"],
                content=les_data["content"],  
                module=module,
                order=j
            )

            for exercise_data in les_data.get("exercises", []):
                Exercise.objects.create(
                    prompt=exercise_data["prompt"],
                    solution=exercise_data.get("solution", ""),
                    lesson=lesson
                )
    return topic