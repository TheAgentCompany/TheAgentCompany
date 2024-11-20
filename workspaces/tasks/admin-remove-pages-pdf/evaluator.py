import os
from PyPDF2 import PdfReader
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader
import logging

# Define expected path for the processed PDF and other criteria
EXPECTED_PDF_PATH = "/workspace/openhands_short.pdf"
EXPECTED_PAGE_COUNT = 17
REFERENCE_CONTENT_FILE = "/utils/expected_openhands_short.pdf"  # Reference file with expected content for comparison


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@grader
def grade_checkpoint1():
    """Check if the output PDF file exists."""
    exists = os.path.exists(EXPECTED_PDF_PATH)
    if exists:
        logging.info(f"Checkpoint 1 passed: {EXPECTED_PDF_PATH} exists.")
    else:
        logging.warning(f"Checkpoint 1 failed: {EXPECTED_PDF_PATH} does not exist.")
    return exists

@grader
def grade_checkpoint2():
    """Check if the output PDF file has exactly 17 pages."""
    if not os.path.exists(EXPECTED_PDF_PATH):
        logging.warning(f"Checkpoint 2 failed: {EXPECTED_PDF_PATH} does not exist.")
        return False
    try:
        pdf = PdfReader(EXPECTED_PDF_PATH)
        page_count = len(pdf.pages)
        if page_count == EXPECTED_PAGE_COUNT:
            logging.info(f"Checkpoint 2 passed: {EXPECTED_PDF_PATH} has {EXPECTED_PAGE_COUNT} pages.")
            return True
        else:
            logging.warning(f"Checkpoint 2 failed: {EXPECTED_PDF_PATH} has {page_count} pages instead of {EXPECTED_PAGE_COUNT}.")
            return False
    except Exception as e:
        logging.error(f"Checkpoint 2 failed: Error reading PDF for page count check - {e}")
        return False

@grader
def grade_checkpoint3():
    """Check if the content of all 17 pages matches the expected content."""
    #No partial credit if some pages match since in real-world a human would need to perform this task again if only some pages match
    if not os.path.exists(EXPECTED_PDF_PATH):
        logging.warning(f"Checkpoint 3 failed: {EXPECTED_PDF_PATH} does not exist.")
        return False
    if not os.path.exists(REFERENCE_CONTENT_FILE):
        logging.warning(f"Checkpoint 3 failed: Reference content file {REFERENCE_CONTENT_FILE} does not exist.")
        return False
    try:
        # Load the generated PDF and expected PDF for comparison
        generated_pdf = PdfReader(EXPECTED_PDF_PATH)
        expected_pdf = PdfReader(REFERENCE_CONTENT_FILE)

        # Check page count
        if len(generated_pdf.pages) != EXPECTED_PAGE_COUNT or len(expected_pdf.pages) != EXPECTED_PAGE_COUNT:
            logging.warning(f"Checkpoint 3 failed: Page count mismatch (generated: {len(generated_pdf.pages)}, expected: {len(expected_pdf.pages)}).")
            return False

        # Compare content on each page
        for i in range(EXPECTED_PAGE_COUNT):
            generated_text = generated_pdf.pages[i].extract_text().strip()
            expected_text = expected_pdf.pages[i].extract_text().strip()
            if generated_text != expected_text:
                logging.warning(f"Checkpoint 3 failed: Mismatch found on page {i + 1}.")
                return False

        logging.info("Checkpoint 3 passed: All pages match the expected content.")
        return True
    except Exception as e:
        logging.error(f"Checkpoint 3 failed: Error reading or comparing PDFs - {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    """Evaluate all checkpoints for the PDF processing task."""
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Verify if the output PDF exists
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Verify if the output PDF has exactly 17 pages 
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    # Checkpoint 3: Verify if all 17 pages match the expected content

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result
