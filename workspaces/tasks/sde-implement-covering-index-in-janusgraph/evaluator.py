import logging
from typing import List
from scoring import Result, Checkpoint
from common import *
import subprocess
import shutil
import re
import os

JANUSGRAPH_DIR = "/workspace/janusgraph"
BENCHMARK_FILE = "janusgraph-benchmark/src/main/java/org/janusgraph/CQLCompositeIndexInlinePropBenchmark.java"

def check_benchmark_file():
    file_path = os.path.join(JANUSGRAPH_DIR, BENCHMARK_FILE)
    if not os.path.exists(file_path):
        logging.error(f"Benchmark file not found: {file_path}")
        return False
    return True

# Verify the performance has been significant improved. Based on my test, it has been improved 140x
@grader
def grade_checkpoint1():
    if not check_benchmark_file():
        return False

    result = subprocess.run(
        ['java', '-cp', 'janusgraph-benchmark/target/janusgraph-benchmark-1.1.0-SNAPSHOT.jar:janusgraph-benchmark/target/lib/*:janusgraph-core/target/janusgraph-core-1.1.0-SNAPSHOT.jar',
         'org.janusgraph.CQLCompositeIndexInlinePropBenchmark'],
        cwd=JANUSGRAPH_DIR,
        capture_output=True,
        text=True
    )

    true_pattern = r'CQLCompositeIndexInlinePropBenchmark.searchVertices\s+true\s+\d+\s+avgt\s+\d+\s+(\d+\.?\d*)'
    false_pattern = r'CQLCompositeIndexInlinePropBenchmark.searchVertices\s+false\s+\d+\s+avgt\s+\d+\s+(\d+\.?\d*)'

    try:
        inline_time = float(re.search(true_pattern, result.stdout).group(1))
        regular_time = float(re.search(false_pattern, result.stdout).group(1))
        improvement = regular_time / inline_time
        
        if improvement >= 10:
            logging.info(f"Performance improvement: {improvement}x")
            return True
        else:
            logging.error(f"Insufficient performance improvement: {improvement}x (required: 10x)")
            return False
    except Exception as e:
        logging.error(f"Failed to parse benchmark results: {e}")
        return False

# Copy the test file in case cheating
def copy_test_file():
    source = "/utils/IndexSerializerTest.java"  
    destination = os.path.join(JANUSGRAPH_DIR, "janusgraph-test/src/test/java/org/janusgraph/graphdb/database/IndexSerializerTest.java")
    try:
        shutil.copy2(source, destination)
        logging.info(f"Copied {source} to {destination}")
        return True
    except Exception as e:
        logging.error(f"Failed to copy test file: {e}")
        return False

@grader
def grade_checkpoint2():
    if not check_benchmark_file():
        return False
    
    if not copy_test_file():
        logging.error("Failed to copy test file in checkpoint2")
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

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    performance_passed = grade_checkpoint1()
    functionality_passed = grade_checkpoint2()

    checkpoints.append(Checkpoint(2, int(performance_passed) * 2))
    checkpoints.append(Checkpoint(1, int(functionality_passed)))

    return result