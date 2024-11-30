import os
from typing import List
from PIL import Image
import io
from io import BytesIO
from scoring import Result, Checkpoint
from common import evaluate_with_llm, grader, check_file_in_owncloud_directory, get_binary_file_content_owncloud, IMAGE_PNG
from pptx import Presentation
import logging
import pandas as pd
from collections import defaultdict



@grader
def grade_checkpoint1():
    csv_path = "stock_cleaned.csv"
    golden_path = "/utils/stock_data.csv"
    dir_name = "Documents/Financials/stock_presentation"

    if not check_file_in_owncloud_directory(csv_path, dir_name):
        return 0
    
    content = get_binary_file_content_owncloud(csv_path, dir_name)
    if not content:
        logging.warning(f"Failed to download content {csv_path}")
        return 0

    try:
        df = pd.read_csv(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read {csv_path}: {e}")
        return 0

    golden_df = pd.read_csv(golden_path)
    return df.equals(golden_df)    
    

@grader
def grade_checkpoint2():
    pptx_path = "stock_analysis.pptx"
    dir_name = "Documents/Financials/stock_presentation"

    if not check_file_in_owncloud_directory(pptx_path, dir_name):
        return 0
    
    content = get_binary_file_content_owncloud(pptx_path, dir_name)
    if not content:
        logging.warning(f"Failed to download content {pptx_path}")
        return 0

    try:
        presentation = Presentation(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read {pptx_path}: {e}")
        return 0

    output_dir = "/utils/figs"
    predicates = [
        "Closing Prices Over Time: Display the stock's closing prices over time to show the overall trend.",
        "Close Price with 50 and 200-Day Moving Averages: Overlay the 50-day and 200-day moving averages onto the closing price plot.",
        "Correlation Between Columns: Visualize the correlation matrix focusing on price, volume, and returns.",
        "Daily Return Distribution: Calculate and plot the daily returns to highlight volatility and risk.",
        "Volume Distribution: Plot the distribution of trade volumes to identify trends in stock interest over time.",
    ]

    os.makedirs(output_dir, exist_ok=True)
    
    # key of results are predicates, value of results are the evaluation results
    results = defaultdict(int)

    for idx, slide in enumerate(presentation.slides, start=1):
        image_found = 0
        for shape in slide.shapes:
            if shape.shape_type == 13:  # Picture type
                image_found += 1
                image = shape.image
                image_bytes = image.blob
                image_stream = io.BytesIO(image_bytes)
                image = Image.open(image_stream)
                image_path = os.path.join(output_dir, f"slide_{idx}_{image_found}.png")
                image.save(image_path, format="PNG")
        if image_found >= 1:
            predicate = predicates[idx - 1]
            for img in range(1, image_found + 1):
                image_path = os.path.join(output_dir, f"slide_{idx}_{img}.png")
                evaluation_result = evaluate_with_llm(None, predicate, image_path=image_path)
                # if there are more than one images on the slide, as long as one image is true, the slide is considered as pass
                if evaluation_result:
                    results[predicate] = 1
                    break

    idx = 0
    for predicate, result in results:
        if result == 0:
            logging.warning(f"Predicate {idx} failed, Predicate: {predicate}")
        idx += 1
    
    return sum([results[pred] for pred in results.keys()])

@grader
def grade_checkpoint3():
    script_path = "stock_analysis_script.md"
    dir_name = "Documents/Financials/stock_presentation"

    if not check_file_in_owncloud_directory(script_path, dir_name):
        return 0
    
    content = get_binary_file_content_owncloud(script_path, dir_name)
    if not content:
        logging.warning(f"Failed to download content {script_path}")
        return 0

    try:
        # save bytesio of the script
        script_content = content.decode("utf-8")
    except Exception as e:
        logging.warning(f"Failed to read {script_path}: {e}")
        return 0


    predicates = [
        "The script contains clear introductions, addressing and greeting the audience, provides presentation context for the audience, analyzes the business context and impact of each graph. The script ends with closing comments expressing gratitude.",
        "The script includes correspondence for each slide below: Slide 1: Closing Prices Over Time, Slide 2: Close Price with 50 and 200-Day Moving Averages, Slide 3: Correlation Between Columns, Slide 4: Daily Return Distribution, Slide 5: Volume Distribution.",
    ]

    results = {pred: evaluate_with_llm(script_content, pred) for pred in predicates}

    for pred, result in results.items():
        logging.info(f"{pred}: {'Pass' if result else 'Fail'}")

    # sum over all pass result as int
    return sum([int(result) for result in results.values()])


def grade_checkpoints(trajectory="") -> Result:
    """
    Evaluate all checkpoints and return the results.
    """
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(5, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint3())))

    return result
