"""
Entrypoint to run evaluation. It calls grade_checkpoints function in
evaluator.py, which is customized per task.
"""
import argparse
import json
import sys
import logging

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
    logging.basicConfig(level=logging.INFO)

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Grade checkpoints from trajectory and save results')
    parser.add_argument('--trajectory_path', required=False, default=None, help='Path to the trajectory file')
    parser.add_argument('--output_path', required=True, default='./output.json', help='Path to save the output JSON')

    # Parse arguments
    args = parser.parse_args()

    trajectory = ""
    try:
        # Check if trajectory path is provided
        if args.trajectory_path is None:
            logging.warning("No trajectory file provided, assuming empty trajectory")
        else:
            trajectory = load_trajectory(args.trajectory_path)
        
        results = grade_checkpoints(trajectory)

        # Verify results is a dict
        if not isinstance(results, dict):
            raise TypeError(f"grade_checkpoints must return a dict, got {type(results)}")

        if not results.get('final_score'):
            raise KeyError(f'grade_checkpoints output must contain a `final_score` field')

        # Save results to JSON file
        with open(args.output_path, 'w') as f:
            json.dump(results, f, indent=4)
            
    except Exception:
        logging.error("Failed to grade the task", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
