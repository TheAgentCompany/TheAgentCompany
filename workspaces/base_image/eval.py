"""
Entrypoint to run evaluation. It calls grade_checkpoints function in
evaluator.py, which is customized per task.
"""
import argparse
import json
import sys
import logging

from evaluator import grade_checkpoints
from scoring import Result, Checkpoint


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

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Grade checkpoints from trajectory and save results')
    parser.add_argument('--trajectory_path', required=False, default=None, help='Path to the trajectory file')
    parser.add_argument('--output_path', required=False, default='./output.json', help='Path to save the output JSON')

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
        with open(args.output_path, 'w') as f:
            json.dump(result_json, f, indent=4)
            
    except Exception:
        logging.error("Failed to grade the task", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
