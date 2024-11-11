from io import BytesIO
from typing import List
from odf.opendocument import load
from odf.element import Node
import logging

from common import llm_complete, get_binary_file_content_nextcloud, create_rocketchat_client, get_rocketchat_channel_history
from scoring import Result, Checkpoint, bonus_for_completing_any

rocket = create_rocketchat_client()

def grade_checkpoint1(trajectory):
    urls = [f"/Documents/Human%20Resources%20Team"]
            
    return any(url in trajectory for url in urls)

def grade_checkpoint2():
    file_name = "Career_Ladder.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    binary_content = get_binary_file_content_nextcloud(file_name, dir_name)

    if binary_content:
        text_content = extract_text_from_odt(binary_content)
        personell_names = [
            "Sarah Johnson", "Li Ming", "Zhang Wei", "Wang Fang", "Mike Chen",
            "Emily Zhou", "Liu Qiang", "Priya Sharma", "Mark Johnson", "Jessica Lee",
            "Chen Xinyi", "David Wong", "Huang Jie", "Sophia Rodriguez", "Alex Turner",
            "Emma Lewis", "Jessica Chen"
        ]

        messages = [{"content": f"You are asked to grade the following draft career ladder from an HR: \"\"{text_content}\"\" \n Is this a valid career ladder design, with all employee names mentioned, and introduces their potential growth paths? The employees are listed below: {" ".join(personell_names)} Please answer 'yes' if it does, or 'no' if it doesn't. ", "role": "user"}]

        try: 
            llm_resonse = llm_complete(messages)
        except Exception as e:
            logging.warning(f"Error: {e}")
            return 0

        if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
            logging.info("Valid career ladder found.")
            score += 1            

        return score
    else:
        logging.warning("Failed to retrieve file content.")
        return 0
    
def grade_checkpoint3():
    messages = get_rocketchat_channel_history(rocket, "hr-announcements")
    if not messages:
        return False
    
    score = 0

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        messages = [{"content": f"You are asked to grade the following message: \"\"{message_text}\"\" \n Is the message about the new career ladder design and asking for suggestions? Please answer 'yes' if it does, or 'no' if it doesn't. ", "role": "user"}]

        try:
            llm_resonse = llm_complete(messages)
        except Exception as e:
            logging.warning(f"Error: {e}")
            return 0
        if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
            logging.info("Correct message found.")
            score += 1
            break
    
    return score
    

def extract_text_from_odt(binary_content):
    odt_file = BytesIO(binary_content)
    document = load(odt_file)

    text_content = ""

    def get_text_from_node(node):
        text = ""
        for child in node.childNodes:
            if isinstance(child, Node):
                if hasattr(child, 'data'):
                    text += child.data + "\n"
                text += get_text_from_node(child)  
        return text

    for elem in document.text.childNodes:
        text_content += get_text_from_node(elem) + "\n"

    return text_content

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result
 