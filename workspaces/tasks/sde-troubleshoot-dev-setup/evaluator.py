from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history
import logging

from packaging.requirements import Requirement
from packaging.version import Version
import re

rocket = create_rocketchat_client()


def grade_checkpoint1(trajectory="") -> bool:
    """Check if agent visited the requirements.txt file in copilot-arena-server."""
    required_url = "/copilot-arena-server/-/blob/main/requirements.txt"
    return required_url in trajectory


def check_requirements_compatibility(base_file, target_file):
    """
    Helper function to check if requirements match target requirements
    Returns: (is_compatible, list of incompatibilities)
    """
    def parse_requirements_file(file_path):
        requirements = {}
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Convert == to >= for parsing
                    req_str = re.sub(r'==', '>=', line)
                    req = Requirement(req_str)
                    requirements[req.name] = req.specifier
        return requirements

    base_reqs = parse_requirements_file(base_file)
    target_reqs = parse_requirements_file(target_file)
    
    incompatibilities = []
    
    for pkg_name, target_spec in target_reqs.items():
        if pkg_name not in base_reqs:
            incompatibilities.append(f"Missing package: {pkg_name}")
            continue
            
        base_spec = base_reqs[pkg_name]
        
        # For each == specification in base, check if it satisfies target
        for spec in base_spec:
            if spec.operator == '>=':
                version = Version(spec.version)
                if not target_spec.contains(version):
                    incompatibilities.append(
                        f"{pkg_name}: Version {version} does not satisfy {target_spec}"
                    )
                    
    return len(incompatibilities) == 0, incompatibilities
    
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

def grade_checkpoint3() -> bool:
    """Check if agent had a conversation with Emily Zhou."""
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")
    return len(messages) > 0

def grade_checkpoint4() -> bool:
    """Check if conversation mentions pandas and scikit-learn version issues."""
    messages = get_rocketchat_personal_chat_history(rocket, "Emily Zhou")    
    combined_messages = " ".join(messages).lower()
    required_keywords = ["pandas", "scikit-learn"]
    return all(keyword in combined_messages for keyword in required_keywords)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Visit requirements.txt
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    
    # Checkpoint 2: Environment alignment
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    
    # Checkpoint 3: Conversation with Emily
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    
    # Checkpoint 4: Specific library discussion
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))

    return result