"""
Entrypoint to run evaluation. It calls grade_checkpoints function in
evaluator.py, which is customized per task.
"""
import os
import base64
import argparse
import json
import sys
import logging

import cryptography
from cryptography.fernet import Fernet

from scoring import Result

def pad_key(key):
    while len(key) < 32:
        key += b'\x00'
    return key[:32]

def decrypt_and_execute():
    decryption_key = os.environ.get('DECRYPTION_KEY')
    if decryption_key is None:
        raise ValueError("DECRYPTION_KEY environment variable is not present")

    byte_string = bytes(decryption_key, 'utf-8')
    padded_key = pad_key(byte_string)
    private_key = base64.urlsafe_b64encode(padded_key)
    
    fernet = Fernet(private_key)
    
    encrypted_file_path = '/utils/evaluator.py.enc'
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_content = encrypted_file.read()
    
    try:
        decrypted_content = fernet.decrypt(encrypted_content)
        logging.info("Decryption successful")
        logging.info(f"Decrypted content length: {len(decrypted_content)}")
        logging.info(f"First 100 characters of decrypted content: {decrypted_content[:100].decode('utf-8')}")
    except cryptography.fernet.InvalidToken as e:
        logging.error(f"Decryption failed: {str(e)}")
        raise RuntimeError("Failed to decrypt evaluator")
    
    # Write decrypted content to a file
    with open('/utils/evaluator.py', 'wb') as f:
        f.write(decrypted_content)
    
    logging.info("Decrypted content written to /utils/evaluator.py")
    
    # Import the evaluator module
    import importlib.util
    spec = importlib.util.spec_from_file_location("evaluator", "/utils/evaluator.py")
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    
    global grade_checkpoints
    grade_checkpoints = evaluator.grade_checkpoints
    
def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # decrypt evaluator.py
    decrypt_and_execute()

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Grade checkpoints from trajectory and save results')
    parser.add_argument('--trajectory_path', required=False, default=None, help='Path to the trajectory file')
    parser.add_argument('--result_path', required=False, default='./result.json', help='Path to save the evaluation result JSON')

    # Parse arguments
    args = parser.parse_args()

    trajectory = ""
    try:
        # Check if trajectory path is provided
        if args.trajectory_path is None:
            logging.warning("No trajectory file provided, assuming empty trajectory")
        else:
            trajectory = load_trajectory(args.trajectory_path)
        
        result = grade_checkpoints(trajectory)

        if not isinstance(result, Result):
            raise TypeError(f"grade_checkpoints must return Result type, got {type(result)}")
        
        if not result.checkpoints:
            raise ValueError(f"Result must have at least one checkpoint, got {result}")

        # Save result to JSON file
        result_json = result.to_dict()
        logging.info(f'result is: {result_json}')
        with open(args.result_path, 'w') as f:
            json.dump(result_json, f, indent=4)
            
    except Exception:
        logging.error("Failed to grade the task", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
