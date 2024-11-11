import os

from typing import List

from PIL import Image
import numpy as np

from scoring import Result, Checkpoint, bonus_for_completing_final

from common import grader

@grader
def check_code_clone():
    # check path exists
    if os.path.exists("/workspace/janusgraph"):
        with open("/workspace/janusgraph/README.MD") as f:
            code_content = f.read()
            if (
                "JanusGraph is a highly scalable [graph database](https://en.wikipedia.org/wiki/Graph_database)",
                "optimized for storing and querying large graphs with billions of vertices and edges distributed",
                "across a multi-machine cluster. JanusGraph is a transactional database that can support thousands",
                "of concurrent users, complex traversals, and analytic graph queries.",
            ) in code_content:
                return True
    return False

@grader
def check_download():
    if os.path.exists("/workspace/janusgraph/new_logo.jpg"):
        image1 = "/workspace/janusgraph/new_logo.jpg"
        image2 = "/utils/reference.jpg"
        print(are_images_equal(image1, image2))

        return True
    else:
        return False

@grader
def check_readme_update():
    # check path exists
    if os.path.exists("/workspace/janusgraph"):
        with open("/workspace/janusgraph/README.MD") as f:
            code_content = f.read()
            if (
                "[![JanusGraph logo](new_logo.jpg)](https://janusgraph.org/)"
                in code_content
            ):
                return True
    return False


def are_images_equal(image_path1, image_path2):
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    return np.all(arr1 == arr2) and arr1.shape == arr2.shape


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, int(check_code_clone())))
    checkpoints.append(Checkpoint(1, int(check_download())))
    checkpoints.append(Checkpoint(1, int(check_readme_update())))
    return result



