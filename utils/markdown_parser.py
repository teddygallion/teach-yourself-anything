import re
import json
from bs4 import BeautifulSoup
import markdown
def parse_learning_path(markdown_content, dry_run=False):

    html_content = markdown.markdown(markdown_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    result = {
        'topic': {
            'title': '',
            'description': ''
        },
        'modules': []
    }
    

    first_heading = soup.find(['h1', 'h2'])
    if first_heading:
        result['topic']['title'] = first_heading.get_text().strip()

    for heading in soup.find_all(['h2', 'h3']):
        if re.match(r'Module \d+:', heading.get_text()):
            module = {
                'title': heading.get_text().strip(),
                'lessons': []
            }
            
            current_node = heading.next_sibling
            while current_node and not (current_node.name in ['h2', 'h3'] and re.match(r'Module \d+:', current_node.get_text())):
                if current_node.name == 'h4' and 'Lesson' in current_node.get_text():
                    lesson = {
                        'title': current_node.get_text().strip(),
                        'key_concepts': [],
                        'exercises': [],
                        'resources': []
                    }
                    
                    content_node = current_node.next_sibling
                    while content_node and not (content_node.name in ['h2', 'h3', 'h4']):
                        if content_node.name == 'ul':
                            current_section = None
                            for li in content_node.find_all('li'):
                                text = li.get_text().strip()
                                
                                if 'Key Concepts:' in text:
                                    current_section = 'key_concepts'
                                    text = text.replace('Key Concepts:', '').strip()
                                elif 'Exercises:' in text:
                                    current_section = 'exercises'
                                    text = text.replace('Exercises:', '').strip()
                                elif 'Recommended Resources:' in text or 'Resources:' in text:
                                    current_section = 'resources'
                                    text = text.replace('Recommended Resources:', '').replace('Resources:', '').strip()
                                elif current_section: 
                                    lesson[current_section].append(text)
                                
                        content_node = content_node.next_sibling
                    
                    module['lessons'].append(lesson)
                
                current_node = current_node.next_sibling
            
            result['modules'].append(module)
    
    if dry_run:
        return result
    else:
        pass