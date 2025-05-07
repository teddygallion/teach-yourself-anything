from markdown import markdown
from bs4 import BeautifulSoup
import re

def markdown_to_text(md):
    html = markdown(md)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()

def parse_roadmap(text):
    modules = []
    current_module = None
    current_lesson = None

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        module_match = re.match(r"\*\*Module \d+: (.+)\*\*", line)
        if module_match:
            current_module = {
                "title": module_match.group(1).strip(),
                "summary": "",
                "lessons": []
            }
            modules.append(current_module)
            current_lesson = None
            continue

        lesson_match = re.match(r"#### Lesson \d+\.\d+: (.+)", line)
        if lesson_match and current_module:
            current_lesson = {
                "title": lesson_match.group(1).strip(),
                "content": "",
                "exercises": [],
                "resources": []
            }
            current_module["lessons"].append(current_lesson)
            continue

        if current_lesson and line.startswith("1.") or line.startswith("2."):
            current_lesson["exercises"].append(line)
            continue

        if current_lesson and ("Book:" in line or "Video:" in line or "Article:" in line):
            current_lesson["resources"].append(line)
            continue


        if current_module and not current_lesson and line:
            current_module["summary"] += line + " "


        if current_lesson and line:
            current_lesson["content"] += line + " "

    return modules


def preview_learning_path(parsed_data):
    for module in parsed_data:
        print(f"\n📦 Module: {module['title']}")
        print(f"   📝 Summary: {module['summary']}")
        for lesson in module['lessons']:
            print(f"\n   🔹 Lesson: {lesson['title']}")
            print(f"      📚 Content: {lesson['content']}")
            print(f"      🧠 Exercises:")
            for exercise in lesson['exercises']:
                print(f"         - {exercise}")
            print(f"      🔗 Resources:")
            for resource in lesson['resources']:
                print(f"         - {resource}")

