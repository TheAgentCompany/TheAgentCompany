import os
import shutil
import logging
import subprocess

from common import grader
from scoring import Result, Checkpoint

REPO_PATH = "/workspace/bustub"
BUSTUB_GIT_LINK = "http://the-agent-company.com:8929/root/bustub.git"
TEST_REPO_PATH = "/workspace/bustub-the-agent-company-evaluation"
TEST_FILE_PATH = TEST_REPO_PATH + "/test/primer/hyperloglog_test.cpp"
HASH_HEAD_PATH = TEST_REPO_PATH + "/src/include/common/util/hash_util.h"
SOURCE_FILES = [
    "/src/include/primer/hyperloglog.h",
    "/src/include/primer/hyperloglog_presto.h",
    "/src/primer/hyperloglog.cpp",
    "/src/primer/hyperloglog_presto.cpp",
]

@grader
def grade_checkpoint1():
    return os.path.exists(REPO_PATH)

@grader
def grade_checkpoint2() -> int:
    """Run 10 tests. Each test is worth 0.5 points. Returns the closest integer to the total score."""
    clone_git_repo_process = subprocess.run(f"git clone {BUSTUB_GIT_LINK} {TEST_REPO_PATH}", shell=True, capture_output=True, text=True)

    print(clone_git_repo_process.stdout)
    if clone_git_repo_process.stderr:
        print(clone_git_repo_process.stderr)

    # Fix os compatibility issue in hash_util.h
    with open(HASH_HEAD_PATH, "r") as file:
        content = file.read()
    content = content.replace("hash = ((hash << 5) ^ (hash >> 27)) ^ bytes[i];", "hash = ((hash << 5) ^ (hash >> 27)) ^ static_cast<signed char>(bytes[i]);")
    with open(HASH_HEAD_PATH, "w") as file:
        file.write(content)

    # Enable all tests
    with open(TEST_FILE_PATH, "r") as file:
        content = file.read()
    modified_content = content.replace("DISABLED_", "")
    with open(TEST_FILE_PATH, "w") as file:
        file.write(modified_content)
    print("Enabled all tests")

    # Copy source files to the test directory
    for source_file in SOURCE_FILES:
        shutil.copy(REPO_PATH + source_file, TEST_REPO_PATH + source_file)
    print("Copied source files")


    command = f"""
        cd {TEST_REPO_PATH} && \
        build_support/packages.sh && \
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
