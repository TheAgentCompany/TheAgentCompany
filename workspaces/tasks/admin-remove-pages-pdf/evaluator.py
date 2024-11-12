import os
from PyPDF2 import PdfReader
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader

# Define expected path for the processed PDF and other criteria
EXPECTED_PDF_PATH = "/workspace/openhands_short.pdf"
EXPECTED_PAGE_COUNT = 17
REFERENCE_CONTENT_FILE = "/utils/expected_openhands_short.pdf"  # Reference file with expected content for comparison
NEXTCLOUD_URL = "apps/files/files/1864?dir=/Documents/Research"

@grader
def grade_checkpoint1(trajectory):
    """Check if the agent visits the 'Documents/Research' directory on NextCloud."""
    return NEXTCLOUD_URL in trajectory

@grader
def grade_checkpoint2():
    """Check if the output PDF file exists."""
    return os.path.exists(EXPECTED_PDF_PATH)

@grader
def grade_checkpoint3():
    """Check if the output PDF file has exactly 17 pages."""
    if not os.path.exists(EXPECTED_PDF_PATH):
        return False
    try:
        pdf = PdfReader(EXPECTED_PDF_PATH)
        return len(pdf.pages) == EXPECTED_PAGE_COUNT
    except Exception as e:
        print(f"Error reading PDF for page count check: {e}")
        return False

@grader
def grade_checkpoint4():
    """Check if the content of all 17 pages matches the expected content."""
    #No partial credit if some pages match since in real-world a human would need to perform this task again if only some pages match
    if not os.path.exists(EXPECTED_PDF_PATH) or not os.path.exists(REFERENCE_CONTENT_FILE):
        return False
    try:
        # Load the generated PDF and expected PDF for comparison
        generated_pdf = PdfReader(EXPECTED_PDF_PATH)
        expected_pdf = PdfReader(REFERENCE_CONTENT_FILE)
        
        if len(generated_pdf.pages) != EXPECTED_PAGE_COUNT or len(expected_pdf.pages) != EXPECTED_PAGE_COUNT:
            return False  # Page count mismatch

        # Compare content on each page
        for i in range(EXPECTED_PAGE_COUNT):
            generated_text = generated_pdf.pages[i].extract_text().strip()
            expected_text = expected_pdf.pages[i].extract_text().strip()
            if generated_text != expected_text:
                return False  # Mismatch found on page i

        return True  # All pages match
    except Exception as e:
        print(f"Error reading or comparing PDFs: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    """Evaluate all checkpoints for the PDF processing task."""
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Verify if the agent accessed the NextCloud directory
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Verify if the output PDF exists
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    # Checkpoint 3: Verify if the output PDF has exactly 17 pages
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    # Checkpoint 4: Verify if all 17 pages match the expected content
    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(1, int(passed4)))

    return result
