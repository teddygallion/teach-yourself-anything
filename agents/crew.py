from .agents import learning_designer_agent, course_creator_agent
from .tasks import get_tasks
from crewai import Crew

def run_learning_path_crew(topic):
    tasks = get_tasks(topic)

    planning_crew = Crew(
        agents=[learning_designer_agent],
        tasks=[tasks[0]]
    )
    roadmap_output = planning_crew.kickoff()

    if not roadmap_output:
        return {
            "topic_title": topic,
            "topic_description": "No output generated.",
            "topic_content": "",
            "modules_data": []
        }

    content_crew = Crew(
        agents=[course_creator_agent],
        tasks=[tasks[1]]
    )
    content_output = content_crew.kickoff()

    return {
        "topic_title": topic,
        "topic_description": "Learning path for " + topic,
        "topic_content": str(roadmap_output),  
        "modules_data": str(content_output) 
    }