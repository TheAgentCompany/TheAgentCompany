from common import evaluate_with_llm, grader, IMAGE_PNG
from scoring import Result, Checkpoint

PIE_CHART_FILE = "/workspace/2011_pie.png"
BAR_CHART_FILE = "/workspace/2016_bar.png"

@grader
def grade_checkpoint1():
    """Validate pie chart"""
    return evaluate_with_llm(
        content="",
        predicate="The picture contains a pie chart, with the value of Garlic being the highest, Sweet potato being the second highest, Chinese vegetables and Kale being the least.",
        image_path=PIE_CHART_FILE
    )

@grader
def grade_checkpoint2():
    """Validate bar chart"""
    return evaluate_with_llm(
        content="",
        predicate="The picture contains a bar chart, with the value of Garlic being the highest, Kale being the second highest, Chinese vegetables and Sweet potato being the least.",
        image_path=BAR_CHART_FILE,
        image_type=IMAGE_PNG
    )

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(2, 2*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(2, 2*int(grade_checkpoint2()))
    return Result([checkpoint1, checkpoint2])

