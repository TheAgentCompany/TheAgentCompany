import os
import logging
from pyzbar.pyzbar import decode
from PIL import Image
import PyPDF2

from common import download_nextcloud_content, grader
from scoring import Result, Checkpoint, bonus_for_completing_final

QR_FILE_PATH = "qrcode_image.png"
JD_FILE_PATH = "jd.pdf"

@grader
def grade_checkpoint1():
    """Check if the file exists"""
    return os.path.exists(QR_FILE_PATH)

@grader
def grade_checkpoint2():
    """Check if the job description is in the downloaded PDF file"""
    try:
        file_url = decode(Image.open(QR_FILE_PATH))[0].data.decode('utf-8')
        if not download_nextcloud_content(file_url, JD_FILE_PATH):
            logging.error(f"Failed to download the file from {file_url}")
            return False
        
        with open(JD_FILE_PATH, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = reader.pages[0].extract_text()
        text = text.lower()
        return "job" in text and "description" in text
    except Exception as e:
        logging.error(f"Error grading checkpoint 2: {e}")
        return False
    return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(1, 1*int(grade_checkpoint2()))
    return Result([checkpoint1, checkpoint2], bonus_for_completing_final)

