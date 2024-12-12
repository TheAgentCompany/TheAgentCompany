import os
import base64
import argparse
import json
import sys
import logging
from cryptography.fernet import Fernet

from scoring import Result

def pad_key(key):
    while len(key) < 32:
        key += b'\x00'
    return key[:32]

def decrypt_and_execute():
    # Get the decryption key from the environment variable
    decryption_key = os.environ.get('DECRYPTION_KEY')
    byte_string = bytes(decryption_key, 'utf-8')
    padded_key = pad_key(byte_string)
    private_key = base64.urlsafe_b64encode(padded_key)

    # Get the Fernet instance
    fernet = Fernet(private_key)

    # Read the encrypted evaluator file
    encrypted_file_path = '/utils/evaluator.py.enc'
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_content = encrypted_file.read()

    try:
        decrypted_content = fernet.decrypt(encrypted_content)
    except cryptography.fernet.InvalidToken:
        # If the decryption fails, silently exit the program
        raise RuntimeError("Failed to decrypt evaluator") 

    # Execute the decrypted content
    exec(decrypted_content.decode('utf-8'), globals())

    # Import the evaluator module after successful decryption
    global grade_checkpoints
    from evaluator import grade_checkpoints
    
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
    decrypt_and_execute()

    logging.basicConfig(level=logging.INFO)

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
