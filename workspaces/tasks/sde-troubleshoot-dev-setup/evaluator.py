from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_any
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, grader
import logging

from packaging.requirements import Requirement
from packaging.version import Version
import re

rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory="") -> bool:
    """Check if agent visited the requirements.txt file in copilot-arena-server."""
    required_url = "/copilot-arena-server/-/blob/main/requirements.txt"
    return required_url in trajectory


def check_requirements_compatibility(base_file, target_file):
    """
    Checks if the requirements in the base_file align with or satisfy the
    constraints in the target_file, and ensures specific versions for pandas
    and scikit-learn.
    Returns: tuple: (is_compatible, list of incompatibilities)
    - is_compatible (bool): True if all requirements in target_file are satisfied by base_file.
    - list of incompatibilities (list): List of string descriptions of incompatibilities.
    """
    KNOWN_MINIMUM_VERSIONS = {
        'pandas': '2.0.0',
        'scikit-learn': '1.5.2'
    }

    def parse_requirements_file(file_path):
        """
        Parse the requirements file and return a dictionary mapping package names
        to their version specifiers.
        """
        requirements = {}
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        req = Requirement(line)
                        requirements[req.name] = req.specifier
                    except Exception as e:
                        logging.warning(f"Failed to parse requirement '{line}': {e}")
        return requirements

    base_reqs = parse_requirements_file(base_file)
    target_reqs = parse_requirements_file(target_file)

    incompatibilities = []

    # Enforce specific versions for pandas and scikit-learn
    for pkg_name, min_version in KNOWN_MINIMUM_VERSIONS.items():
        if pkg_name in base_reqs:
            specifier = base_reqs[pkg_name]
            if not specifier.contains(Version(min_version)):
                incompatibilities.append(
                    f"{pkg_name}: Version {min_version} is required, but found {specifier}"
                )
        else:
            incompatibilities.append(f"{pkg_name} is missing from {base_file}")

    # Check general compatibility with target requirements
    for pkg_name, target_spec in target_reqs.items():
        if pkg_name not in base_reqs:
            incompatibilities.append(f"Missing package: {pkg_name}")
            continue

        base_spec = base_reqs[pkg_name]

        # Check if the base specifier satisfies the target specifier
        for spec in base_spec:
            if spec.operator == '>=':
                version = Version(spec.version)
                if not target_spec.contains(version):
                    incompatibilities.append(
                        f"{pkg_name}: Version {version} does not satisfy {target_spec}"
                    )

    return len(incompatibilities) == 0, incompatibilities

@grader
def grade_checkpoint2() -> bool:
    """Compare myenv.txt with requirements.txt for alignment."""
    try:
        # Use the helper function to check compatibility
        is_compatible, incompatibilities = check_requirements_compatibility(
            '/workspace/myenv.txt',
            '/utils/requirements.txt'
        )
        if not is_compatible:
            logging.warning(f"Requirements incompatibilities found: {incompatibilities}")
        return is_compatible
        
    except Exception as e:
        return False


@grader
def grade_checkpoint3() -> bool:
    """Check if agent had a conversation with Emily Zhou."""
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")
    return len(messages) > 0

@grader
def grade_checkpoint4() -> bool:
    """Check if conversation mentions pandas and scikit-learn version issues."""
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")    
    combined_messages = " ".join(messages).lower()
    required_keywords = ["pandas", "scikit-learn"]
    return all(keyword in combined_messages for keyword in required_keywords)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    # Checkpoint 1: Visit requirements.txt
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    
    # Checkpoint 2: Environment alignment
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    
    # Checkpoint 3: Conversation with Emily
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    
    # Checkpoint 4: Specific library discussion
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))

    return result