import os
import logging
from typing import List
from pdf2image import convert_from_path 
from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################


rocket = create_rocketchat_client()

############################# helper functions #####################################

def pdf_to_png(pdf_path, output_path):
    try:
        # Convert PDF to PNG
        images = convert_from_path(pdf_path)
        if images:
            # Save the first page as PNG
            images[0].save(output_path, 'PNG')
            return output_path
    except Exception as e:
        logging.error(f"Error converting PDF to PNG: {str(e)}")
        return None

def compare_figures(index):
    query = 'Are the 2 images roughly the same in terms of appearance and the information represented?'
    generated_png = pdf_to_png(f'/workspace/figure{index}.pdf',f'/workspace/figure{index}.png')
    if not generated_png:
        return False
    return compare_images_with_llm(generated_png,f'/eval_data/figure{index}.png',query)

def is_pdf(file_path):
    if len(file_path.split('.'))<2:
        logging.warning(f'Filename issues in {file_path}')
        return False

    #Check extension
    if not file_path.split('.')[1].strip() == 'pdf':
        return False

    try:
        #Check if file is actually in pdf format
        with open(file_path, 'rb') as file:
            header = file.read(5)
            return header.startswith(b'%PDF-')

    except FileNotFoundError:
        logging.warning(f"The file {file_path} was not found")
        return False
    except Exception as e:
        logging.error(f"Error while checking file {file_path}: {str(e)}")
        return False
    
def compare_tables(index):
    query = 'Are the 2 tables roughly similar in terms of appearance and represent the same information?'
    if not os.path.exists(f'/workspace/table{index}.pdf'):
        return False
    generated_png = pdf_to_png(f'/workspace/table{index}.pdf',f'/workspace/table{index}.png')
    if not generated_png:
        return False
    return compare_images_with_llm(generated_png,f'/eval_data/table{index}.png',query)

def table_code_overlap(file_path1:str, file_path2:str, threshold:float):
    try:
        with open(file_path1,'r') as file:
            content1 = file.read()
        # Extract content between first \begin and last \end
        start1 = content1.find('\\begin{table}')
        end1 = content1.rfind('\\end{table}') + 11  # +4 to include '\end'
        content1 = content1[start1:end1] if start1 != -1 and end1 != 10 else content1
        
        with open(file_path2,'r') as file:
            content2 = file.read()
        # Extract content between first \begin and last \end    
        start2 = content2.find('\\begin{table}')
        end2 = content2.rfind('\\end{table}') + 11  # +4 to include '\end'
        content2 = content2[start2:end2] if start2 != -1 and end2 != 10 else content2
        
        overall_similarity = SequenceMatcher(None, content1, content2).ratio()
        return overall_similarity >= threshold
    except FileNotFoundError:
        logging.warning('File not found')
        return False
    except Exception as e:
        logging.error(f'Error when comparing file content: {e}')
        return False
    
def verify_image_file(image_path: str) -> bool:
    """
    Verifies if a file exists and is a valid JPEG/JPG or PNG image.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if file exists and is a valid JPEG/JPG or PNG image, False otherwise
    """
    if not image_path or not os.path.isfile(image_path):
        logging.warning(f"Image file not provided or does not exist: {image_path}")
        return False
    
    try:
        with open(image_path, "rb") as f:
            # Try reading first few bytes to check if it's a valid image
            header = f.read(8)
            # Check for JPEG/JPG or PNG signatures
            if not (header.startswith(b'\xFF\xD8\xFF') or  # JPEG/JPG (both use same signature)
                   header.startswith(b'\x89PNG\r\n')):     # PNG
                logging.warning(f"Invalid image format for {image_path}. Only JPEG/JPG and PNG are supported.")
                return False
        return True
    except Exception as e:
        logging.error(f"Failed to read image file {image_path}: {e}")
        return False


def compare_images_with_llm(image_path1: str = None, image_path2: str = None, query='', additional_prompt: str = ''):
    """
    Evaluates if  2 images based on the query, judged by LLM
    """

    # Validate both images
    if not verify_image_file(image_path1) or not verify_image_file(image_path2):
        return False

    query += f' Please answer "yes" if it does, or "no" if it does not. {additional_prompt}'

    try:
        with open(image_path1, "rb") as f:
            base64_image1 = base64.b64encode(f.read()).decode('utf-8')
        with open(image_path2, "rb") as f:
            base64_image2 = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Failed to read image: {e}")
        return False

    content = [
        {
            "type": "text",
            "text": query
        }
    ]
    content.extend([{
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image1}"
        }
    },
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image2}"
        }
    }])

    try:
        # Construct LLM query
        llm_messages = [{
            "role": "user",
            "content": content
        }]

        # Call LLM for evaluation
        try:    
            llm_response = llm_complete(llm_messages)
            logging.info("LLM evaluation completed", extra={"response": llm_response})
        except Exception as e:
            logging.error(f"Failed to evaluate images: {str(e)}", exc_info=True)
            return False

        # Extract and process response
        content = llm_response["choices"][0]["message"]["content"].lower().strip()

        # Evaluate result
        result = "yes" in content
        if result:
            logging.info(f'Image comparisons evaluated to "{result}"')
        else:
            logging.warning(f'Image comparisons evaluated to "{result}"')

        return result

    except KeyError as e:
        logging.error("Invalid LLM response structure", exc_info=True)
        return False

    except Exception as e:
        logging.error(f"Failed to evaluate message: {str(e)}", exc_info=True)
        return False


############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    return is_pdf('/workspace/figure2.pdf') and compare_figures(2)

@grader
def grade_checkpoint2():
    return is_pdf('/workspace/figure3.pdf') and compare_figures(3)

@grader
def grade_checkpoint3():
    return is_pdf('/workspace/figure4.pdf') and compare_figures(4)

@grader
def grade_checkpoint4():
    fig2 = check_rocketchat_message_posted(rocket,'general',['/workspace/figure2.pdf'])
    fig3 = check_rocketchat_message_posted(rocket, 'general', ['/workspace/figure3.pdf'])
    fig4 = check_rocketchat_message_posted(rocket, 'general', ['/workspace/figure4.pdf'])
    return fig2 and fig3 and fig4

@grader
def grade_checkpoint5():
    return table_code_overlap('/workspace/table1.tex','/eval_data/table1.tex',0.9) and compare_tables(1)

@grader
def grade_checkpoint6():
    return table_code_overlap('/workspace/table2.tex','/eval_data/table2.tex',0.9) and compare_tables(2)

@grader
def grade_checkpoint7():
    return table_code_overlap('/workspace/table3.tex','/eval_data/table3.tex',0.9) and compare_tables(3)

@grader
def grade_checkpoint8():
    table1_tex = not check_rocketchat_message_posted(rocket,'general',['/workspace/table1.tex'])
    table2_tex = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table2.tex'])
    table3_tex = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table3.tex'])
    table1_pdf = not check_rocketchat_message_posted(rocket,'general',['/workspace/table1.pdf'])
    table2_pdf = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table2.pdf'])
    table3_pdf = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table3.pdf'])
    return table1_tex and table2_tex and table3_tex and table1_pdf and table2_pdf and table3_pdf



def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint6())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint7())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint8())))

    return result
