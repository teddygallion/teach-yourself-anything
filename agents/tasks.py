from crewai import Task
from .agents import learning_designer_agent, course_creator_agent

def get_tasks(topic: str):
    planning_prompt = (
        f"Create a structured learning roadmap for the topic: '{topic}'. "
        f"Divide the roadmap into 4–6 logical modules. Each module should have a title and a 2–3 sentence summary."
    )

    content_prompt = (
        f"Based on the learning roadmap for '{topic}', create detailed lesson content for each module. "
        f"Each lesson should include a lesson title, key concepts, 1–2 exercises, and recommended resources (books, videos, or articles)."
    )

    return [
        Task(
            description=planning_prompt,
            expected_output="A roadmap with titled modules and brief descriptions.",
            agent=learning_designer_agent
        ),
        Task(
            description=content_prompt,
            expected_output="Complete lesson content organized by module.",
            agent=course_creator_agent
        )
    ]
