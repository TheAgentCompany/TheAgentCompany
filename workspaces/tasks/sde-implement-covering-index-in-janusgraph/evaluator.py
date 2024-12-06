import logging
from typing import List
from scoring import Result, Checkpoint
from common import *
import subprocess
import shutil
import re
import os

JANUSGRAPH_DIR = "/workspace/janusgraph"

def copy_test_file():
    source = "/utils/IndexSerializerTest.java"  
    destination = os.path.join(JANUSGRAPH_DIR, "janusgraph-test/src/test/java/org/janusgraph/graphdb/database/IndexSerializerTest.java")
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        logging.error(f"Failed to copy test file: {e}")
        return False

@grader
def grade_checkpoint1():
    if not copy_test_file():
        logging.error("Failed to copy test file in checkpoint1")
        return False
    
    result = subprocess.run(
        ['mvn', 'test', '-pl', 'janusgraph-test', '-Dtest=IndexSerializerTest'],
        cwd=JANUSGRAPH_DIR,
        capture_output=True,
        text=True
    )

    output = result.stdout + "\n" + result.stderr
        
    if "No tests were run" in output:
        logging.warning("No tests were run. Command may be invalid.")
        return False
        
    if "BUILD SUCCESS" in output:
        logging.info("All tests passed.")
        return True
    else:
        logging.error("Tests failed or unexpected output.")
        logging.error(output)
        return False

def run_benchmark():
    try:
        result = subprocess.run(
            ['java', '-cp', 'janusgraph-benchmark/target/janusgraph-benchmark-1.1.0-SNAPSHOT.jar:janusgraph-benchmark/target/lib/*:janusgraph-core/target/janusgraph-core-1.1.0-SNAPSHOT.jar',
             'org.janusgraph.CQLCompositeIndexInlinePropBenchmark'],
            cwd=JANUSGRAPH_DIR,
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        logging.error(f"Error running benchmark: {str(e)}")
        return None

@grader
def grade_checkpoint2():
    result = getattr(grade_checkpoint2, 'benchmark_result', None)
    if result is None:
        result = run_benchmark()
        setattr(grade_checkpoint2, 'benchmark_result', result)
    
    if result is None:
        return False
        
    pattern = r'CQLCompositeIndexInlinePropBenchmark.searchVertices\s+(\w+)\s+5000\s+avgt\s+\d+\s+\d+\.\d+'
    results = re.findall(pattern, result)
    
    if 'true' in results and 'false' in results:
        return True
    else:
        logging.error("Missing benchmark results")
        return False

@grader
def grade_checkpoint3():
    result = getattr(grade_checkpoint2, 'benchmark_result', None)
    if result is None:
        logging.error("No benchmark result available")
        return False
    
    try:
        true_pattern = r'CQLCompositeIndexInlinePropBenchmark.searchVertices\s+true\s+\d+\s+avgt\s+\d+\s+(\d+\.?\d*)'
        false_pattern = r'CQLCompositeIndexInlinePropBenchmark.searchVertices\s+false\s+\d+\s+avgt\s+\d+\s+(\d+\.?\d*)'

        inline_time = float(re.search(true_pattern, result).group(1))
        regular_time = float(re.search(false_pattern, result).group(1))
        improvement = regular_time / inline_time
        
        logging.info(f"Performance improvement: {improvement}x")
        return improvement >= 10
        
    except Exception as e:
        logging.error(f"Failed to parse benchmark results: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoint1_passed = grade_checkpoint1()
    checkpoint2_passed = grade_checkpoint2()
    checkpoint3_passed = grade_checkpoint3() if checkpoint2_passed else False
    
    # only grant checkpoint1 points if the task is complete. In other words,
    # we don't give free credit for doing nothing.
    checkpoints.append(Checkpoint(1, int(checkpoint1_passed and checkpoint2_passed and checkpoint3_passed)))
    checkpoints.append(Checkpoint(1, int(checkpoint2_passed)))
    checkpoints.append(Checkpoint(1, int(checkpoint3_passed)))
    
    return result