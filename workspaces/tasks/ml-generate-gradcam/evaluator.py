import requests
import os
import logging
from datetime import datetime, timezone
from typing import List
import json
import torch
import torch.nn.functional as F

from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################


############################# helper functions #####################################
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
    """Compare the visual similarity of generated GradCAM visualizations"""
    try:
        return compare_images_with_llm(
            '/workspace/gradcam_output.jpg', 
            '/eval_data/reference_gradcam.jpg',
            'Do these two GradCAM visualizations highlight similar regions in the image?',
            'Focus on the regions highlighted in red/orange and their intensity patterns.'
        )
    except Exception as e:
        logging.error(f"Failed to compare GradCAM visualizations: {e}")
        return False

@grader
def grade_checkpoint2():
    """Check if both GradCAMs are highlighting semantically similar features"""
    if not os.path.exists('/workspace/gradcam_explanation.txt'):
        logging.warning("GradCAM explanation file not found")
        return False
    with open('/workspace/gradcam_explanation.txt', 'r') as f:
        gradcam_explanation = f.read()
    try:
        return evaluate_with_llm(
            gradcam_explanation,
            'The model made the prediction by focusing on the head area to a high degree and also the body to a lower degree.',
        )
    except Exception as e:
        logging.error(f"Failed to compare GradCAM explanations: {e}")
        return False

@grader
def grade_checkpoint3():
    """Compare the similarity of gradients"""
    try:
        # Load saved gradients
        student_gradients = torch.load('/workspace/raw_gradients.pt')
        reference_gradients = torch.load('/eval_data/reference_gradients.pt')
        
        # Calculate cosine similarity
        similarity = F.cosine_similarity(
            student_gradients.flatten(), 
            reference_gradients.flatten(), 
            dim=0
        )
        
        # Consider them similar if cosine similarity is above 0.8
        return similarity.item() > 0.8
    except Exception as e:
        logging.error(f"Failed to compare gradients: {e}")
        return False

@grader
def grade_checkpoint4():
    """Compare the similarity of activations"""
    try:
        # Load saved activations
        student_activations = torch.load('/workspace/raw_activations.pt')
        reference_activations = torch.load('/eval_data/reference_activations.pt')
        
        # Calculate cosine similarity
        similarity = F.cosine_similarity(
            student_activations.flatten(), 
            reference_activations.flatten(), 
            dim=0
        )
        
        # Consider them similar if cosine similarity is above 0.8
        return similarity.item() > 0.8
    except Exception as e:
        logging.error(f"Failed to compare activations: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))

    return result
