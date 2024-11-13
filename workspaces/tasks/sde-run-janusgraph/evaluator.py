import logging
import os
import subprocess
import json
from typing import List
from scoring import Result, Checkpoint
from common import *

# Check if JanusGraph repo is cloned
@grader
def grade_checkpoint1():
    return check_repo_exists('janusgraph')

# Check if binary file is built
@grader
def grade_checkpoint2():
    try:
        # Find all files in the janusgraph-dist/target directory
        target_dir = "/workspace/janusgraph/janusgraph-dist/target"
        if not os.path.exists(target_dir):
            return False
        
        files = os.listdir(target_dir)
        # Check if any file matches the pattern janusgraph-*.zip
        return any(file.startswith("janusgraph-") and file.endswith(".zip") for file in files)
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check if JanusGraph Server is running as HTTP endpoint
@grader
def grade_checkpoint3():
    try:
        cmd = '''curl -XPOST -Hcontent-type:application/json -d '{"gremlin":"g.V().count()"}' http://127.0.0.1:8182'''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return False
            
        response = json.loads(result.stdout)
        # Check if response has the expected structure and status code 200
        return (response.get("status", {}).get("code") == 200 and
                isinstance(response.get("result", {}).get("data", {}).get("@value"), list))
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoint1_passed = grade_checkpoint1()
    checkpoint2_passed = grade_checkpoint2()
    checkpoint3_passed = grade_checkpoint3()

    checkpoints.append(Checkpoint(1, int(checkpoint1_passed)))
    checkpoints.append(Checkpoint(2, int(checkpoint2_passed) * 2))
    
    # If checkpoint3 passes, give full points
    if checkpoint3_passed:
        checkpoints.append(Checkpoint(3, 3))
    else:
        checkpoints.append(Checkpoint(3, 0))
    
    return result