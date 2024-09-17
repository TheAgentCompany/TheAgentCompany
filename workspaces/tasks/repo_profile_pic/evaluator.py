import os

from PIL import Image
import numpy as np

HOSTNAME = os.getenv("HOSTNAME")
GITLAB_PORT = os.getenv("GITLAB_PORT")
GITLAB_USER = "root"
GITLAB_URL = f"http://{HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"


def check_url(browser_logs):
    return (
        f"{GITLAB_URL}/root/janusgraph"
        and "https://www.pexels.com/photo/a-bee-is-on-a-sunflower-in-a-field-27220813/"
        in browser_logs
    )


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


def check_download():
    if os.path.exists("/workspace/janusgraph/new_logo.jpg"):
        image1 = "/workspace/janusgraph/new_logo.jpg"
        image2 = "/utils/reference.jpg"
        print(are_images_equal(image1, image2))

        return True
    else:
        return False


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


if __name__ == "__main__":
    print(
        check_url(
            [
                f"ACTION: goto('{GITLAB_URL}/root/api-server')",
                "ACTION: goto('https://www.pexels.com/photo/a-bee-is-on-a-sunflower-in-a-field-27220813/')",
            ]
        )
    )
    print(check_code_clone())
    print(check_download())
    print(check_readme_update())
