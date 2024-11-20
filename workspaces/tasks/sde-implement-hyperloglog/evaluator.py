import os
import shutil
import logging
import subprocess

from common import grader
from scoring import Result, Checkpoint

REPO_PATH = "/workspace/bustub"
BUSTUB_GIT_LINK = "http://the-agent-company.com:8929/root/bustub.git"
TEST_FILE_PATH = REPO_PATH + "/test/primer/hyperloglog_test.cpp"
TEST_FILE_BACKUP_PATH = "/utils/hyperloglog_test.cpp"

@grader
def grade_checkpoint1():
    return os.path.exists(REPO_PATH)

@grader
def grade_checkpoint2() -> int:
    """Run 10 tests. Each test is worth 0.5 points. Returns the closest integer to the total score."""
    shutil.copy(TEST_FILE_BACKUP_PATH, TEST_FILE_PATH)
    logging.info("Copied test file")

    command = f"""
        cd {REPO_PATH} && \
        rm -rf build && \
        mkdir -p build && \
        cd build && \
        cmake -DCMAKE_BUILD_TYPE=Debug .. && \
        make -j$(nproc) hyperloglog_test && \
        ./test/hyperloglog_test
    """

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout = ""
    for line in process.stdout:
        print(line, end="")
        stdout += line

    process.wait()

    if process.returncode != 0:
        for line in process.stderr:
            print(line, end="")

    passed_tests = stdout.count("[       OK ]")
    return passed_tests // 2
    

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(5, int(grade_checkpoint2()))
    return Result([checkpoint1, checkpoint2])
