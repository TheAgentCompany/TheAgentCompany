#!/usr/bin/env python3
"""
Script to generate task names and their corresponding image URLs.
Based on the logic from evaluation/run_eval.sh
"""

import os
import json
import argparse
import re
from pathlib import Path


def check_llm_functions_in_evaluator(evaluator_path):
    """
    Check if evaluator.py contains any of the three LLM function calls.
    
    Args:
        evaluator_path (Path): Path to the evaluator.py file
        
    Returns:
        bool: True if any LLM function is found, False otherwise
    """
    if not evaluator_path.exists():
        return False
    
    try:
        with open(evaluator_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for the three LLM function calls
        llm_functions = [
            r'\bllm_complete\b',
            r'\bevaluate_with_llm\b', 
            r'\bevaluate_chat_history_with_llm\b'
        ]
        
        for pattern in llm_functions:
            if re.search(pattern, content):
                return True
        
        return False
    except Exception as e:
        print(f"Warning: Could not read {evaluator_path}: {e}")
        return False


def generate_task_images(tasks_dir, version="1.0.0", output_file=None, exclude_scenarios=False, exclude_llm_functions=False):
    """
    Generate a JSON file containing task names and their corresponding image URLs.
    
    Args:
        tasks_dir (str): Path to the tasks directory
        version (str): Version tag for the images
        output_file (str): Output JSON file path (optional)
        exclude_scenarios (bool): Whether to exclude tasks with scenarios.json files
        exclude_llm_functions (bool): Whether to exclude tasks with LLM function calls in evaluator.py
    """
    tasks_dir_path = Path(tasks_dir)
    
    if not tasks_dir_path.exists():
        raise FileNotFoundError(f"Tasks directory not found: {tasks_dir}")
    
    task_images = []
    excluded_tasks = []
    excluded_scenarios_tasks = []
    excluded_llm_tasks = []
    
    # Iterate through each directory in tasks
    for task_dir in tasks_dir_path.iterdir():
        if task_dir.is_dir():
            task_name = task_dir.name
            should_exclude = False
            exclude_reason = []
            
            # Check if scenarios.json exists in the task directory
            scenarios_file = task_dir / "scenarios.json"
            if exclude_scenarios and scenarios_file.exists():
                excluded_scenarios_tasks.append(task_name)
                exclude_reason.append("scenarios.json")
                should_exclude = True
            
            # Check if evaluator.py contains LLM function calls
            evaluator_file = task_dir / "evaluator.py"
            if exclude_llm_functions and check_llm_functions_in_evaluator(evaluator_file):
                excluded_llm_tasks.append(task_name)
                exclude_reason.append("LLM functions")
                should_exclude = True
            
            if should_exclude:
                excluded_tasks.append({
                    "task_name": task_name,
                    "reasons": exclude_reason
                })
                continue
            
            # Generate image URL based on the logic from run_eval.sh
            image_url = f"ghcr.io/theagentcompany/{task_name}-image:{version}"
            
            task_info = {
                "task_name": task_name,
                "image_url": image_url,
                "version": version
            }
            
            task_images.append(task_info)
    
    # Sort by task name for consistent output
    task_images.sort(key=lambda x: x["task_name"])
    
    # Create the final JSON structure
    result = {
        "version": version,
        "total_tasks": len(task_images),
        "exclude_scenarios": exclude_scenarios,
        "exclude_llm_functions": exclude_llm_functions
    }
    
    if excluded_tasks:
        result["excluded_tasks"] = sorted(excluded_tasks, key=lambda x: x["task_name"])
        result["excluded_count"] = len(excluded_tasks)
        
        if exclude_scenarios and excluded_scenarios_tasks:
            result["excluded_scenarios_count"] = len(excluded_scenarios_tasks)
            result["excluded_scenarios_tasks"] = sorted(excluded_scenarios_tasks)
        
        if exclude_llm_functions and excluded_llm_tasks:
            result["excluded_llm_count"] = len(excluded_llm_tasks)
            result["excluded_llm_tasks"] = sorted(excluded_llm_tasks)
    
    result["tasks"] = task_images
    
    # Output to file or stdout
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Generated {len(task_images)} task images to: {output_file}")
        if excluded_tasks:
            print(f"Excluded {len(excluded_tasks)} tasks:")
            if exclude_scenarios and excluded_scenarios_tasks:
                print(f"  - {len(excluded_scenarios_tasks)} tasks with scenarios.json files")
            if exclude_llm_functions and excluded_llm_tasks:
                print(f"  - {len(excluded_llm_tasks)} tasks with LLM function calls")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result


def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    # Calculate the path to workspaces/tasks relative to the script location
    default_tasks_dir = script_dir / ".." / "workspaces" / "tasks"
    
    parser = argparse.ArgumentParser(
        description="Generate task names and their corresponding image URLs"
    )
    parser.add_argument(
        "--tasks-dir",
        default=str(default_tasks_dir),
        help=f"Path to the tasks directory (default: {default_tasks_dir})"
    )
    parser.add_argument(
        "--version",
        default="1.0.0",
        help="Version tag for the images (default: 1.0.0)"
    )
    parser.add_argument(
        "--output",
        help="Output JSON file path (if not specified, prints to stdout)"
    )
    parser.add_argument(
        "--exclude-scenarios",
        action="store_true",
        help="Exclude tasks that have scenarios.json files"
    )
    parser.add_argument(
        "--exclude-llm-functions",
        action="store_true",
        help="Exclude tasks that have LLM function calls (llm_complete, evaluate_with_llm, evaluate_chat_history_with_llm) in evaluator.py"
    )
    
    args = parser.parse_args()
    
    try:
        generate_task_images(
            args.tasks_dir, 
            args.version, 
            args.output, 
            args.exclude_scenarios,
            args.exclude_llm_functions
        )
    except Exception as e:
        print(f"Error: {e}", file=os.sys.stderr)
        exit(1)


if __name__ == "__main__":
    main() 