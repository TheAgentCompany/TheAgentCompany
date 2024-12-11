import json
import glob
import re
import os
import sys
from typing import Dict, Tuple

def analyze_eval_json_file(filepath: str) -> Tuple[int, int]:
    """
    Analyze a single eval JSON file and extract the total and result from final_score.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Tuple containing (total, result) from final_score
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        final_score = data.get('final_score', {})
        return (
            final_score.get('total', 0),
            final_score.get('result', 0)
        )
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {filepath}: {e}")
        return (0, 0)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return (0, 0)

def analyze_state_json_file(filepath: str) -> Tuple[int, float]:
    """
    Analyze a single final state JSON file and extract the steps and cost.
    TODO: this is not a real JSON file at the moment, but a custom str format,
    so we need to parse it manually.

    Args:
        filepath: Path to the JSON file

    Returns:
        Tuple containing (steps, cost)
    """
    try:
        with open(filepath, 'r') as f:
            data = f.read()

        if 'iteration=' in data:
            iteration_part = data.split('iteration=')[1]
            steps = int(iteration_part.split(',')[0])

        if "accumulated_cost': " in data:
            cost_part = data.split("accumulated_cost': ")[1]
            cost = float(cost_part.split(',')[0])

        return (steps, cost)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return (0, 0)

def analyze_folder(folder_path: str) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, float]]]:
    """
    Analyze all eval_*.json & state_*.json files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing JSON files
        
    Returns:
        Two dictionaries:
        - eval_results: Dictionary with filename as key and (total, result) tuple as value
        - state_results: Dictionary with filename as key and (steps, cost) tuple as value
    """
    eval_results = {}
    state_results = {}
    eval_pattern = os.path.join(folder_path, "eval_*.json")
    state_pattern = os.path.join(folder_path, "state_*.json")
    
    for filepath in glob.glob(eval_pattern):
        filename = os.path.basename(filepath)
        total, result = analyze_eval_json_file(filepath)
        key = re.search(r"eval_(.+)\.json", filename).group(1)
        eval_results[key] = (total, result)
    
    for filepath in glob.glob(state_pattern):
        filename = os.path.basename(filepath)
        steps, cost = analyze_state_json_file(filepath)
        key = re.search(r"state_(.+)\.json", filename).group(1)
        state_results[key] = (steps, cost)

    return eval_results, state_results

def calculate_score(total: int, result: int) -> float:
    """
    Calculate the score as a number between 0 and 1.

    Formula: score = (result / total) * 0.5 + (result // total) * 0.5
    Explanation:
    - (result / total) * 0.5: This is the completion ratio, scaled down to a 0-0.5 range.
    - (result // total) * 0.5: This is a binary score indicating whether the task was completed or not.
    
    Args:
        total: Total possible points
        result: Actual points achieved
        
    Returns:
        Score as a number between 0 and 1
    """
    return (result / total * 0.5) + (result // total * 0.5)

def is_perfect_completion(total: int, result: int) -> bool:
    """
    Check if the task achieved perfect completion.
    
    Args:
        total: Total possible points
        result: Actual points achieved
        
    Returns:
        True if result equals total, False otherwise
    """
    return total > 0 and total == result

def main():
    if len(sys.argv) != 2:
        print("Usage: python summarise_results.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        sys.exit(1)
    
    eval_results, state_results = analyze_folder(folder_path)
    
    if not eval_results:
        print(f"No eval_*.json files found in {folder_path}")
        return

    # Create list of results with completion ratios for sorting
    detailed_results = [
        (
            task_name,
            total,
            result,
            calculate_score(total, result),
            is_perfect_completion(total, result)
        )
        for task_name, (total, result) in eval_results.items()
    ]
    
    # Sort by score in descending order
    detailed_results.sort(key=lambda x: (-x[3], x[0]))
    
    # Calculate perfect completion stats
    perfect_completions = sum(1 for _, _, _, _, is_perfect in detailed_results if is_perfect)
    
    # Print header
    print("\n# Evaluation Results Report")
    print("\n## Results per File")
    print("\n*Sorted by score (⭐ indicates perfect completion)*\n")
    
    # Print table header
    print("| Filename | Total | Result | Score | Steps | Cost |")
    print("|----------|--------|---------|-------|-------|------|")
    
    # Print individual file results
    for task_name, total, result, score, is_perfect in detailed_results:
        perfect_marker = " ⭐" if is_perfect else ""
        print(f"| {task_name} | {total:,} | {result:,} | {score:.2f}{perfect_marker} | {state_results[task_name][0]} | {state_results[task_name][1]:.2f} |")
    
    # Print summary section
    print("\n## Summary\n")
    print(f"**Tasks Evaluated:** {len(eval_results)}\n")
    print(f"**Perfect Completions:** {perfect_completions}/{len(eval_results)} ({(perfect_completions/len(eval_results)*100):.1f}%)\n")
    
    overall_score = sum(score for _, _, _, score, _ in detailed_results) / len(detailed_results) * 100
    avg_steps = sum(steps for steps, _ in state_results.values()) / len(state_results)
    avg_cost = sum(cost for _, cost in state_results.values()) / len(state_results)
    print(f"**Overall Score:** {overall_score:.2f}%\n")
    print(f"**Average Steps:** {avg_steps:.2f}\n")
    print(f"**Average Cost (USD):** {avg_cost:.2f}\n")

    # Additional statistics
    if detailed_results:
        highest_score = max(score for _, _, _, score, _ in detailed_results)
        lowest_score = min(score for _, _, _, score, _ in detailed_results)
        median_score = detailed_results[len(detailed_results) // 2][3]
        avg_score = sum(score for _, _, _, score, _ in detailed_results) / len(detailed_results)
        
        print("\n## Statistics\n")
        print("| Metric | Value |")
        print("|---------|--------|")
        print(f"| Highest Task Score | {highest_score:.2f} |")
        print(f"| Lowest Task Score | {lowest_score:.2f} |")
        print(f"| Median Task Score | {median_score:.2f} |")
        print(f"| Average Task Score | {avg_score:.2f} |")

if __name__ == "__main__":
    main()