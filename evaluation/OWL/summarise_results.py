import json
import glob
import os
import yaml
import sys
from typing import Dict, Tuple

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculate the cost of the model call.
    """
    if "claude-3-5-sonnet" in model.lower():
        # https://www.anthropic.com/pricing#anthropic-api, accessed 12/11/2024
        return 0.000003 * prompt_tokens + 0.000015 * completion_tokens
    elif 'claude-3-7-sonnet' in model.lower():
        # https://www.anthropic.com/pricing#anthropic-api, accessed 05/08/2025
        return 0.000003 * prompt_tokens + 0.000015 * completion_tokens
    elif "gpt-4o" in model.lower():
        # https://openai.com/api/pricing/, accessed 12/11/2024
        return 0.0000025 * prompt_tokens + 0.00001 * completion_tokens
    elif "gemini-1.5-pro" in model.lower():
        # https://ai.google.dev/pricing#1_5pro, accessed 12/11/2024
        # assuming prompts up to 128k tokens
        cost = 0.00000125 * prompt_tokens + 0.000005 * completion_tokens
        if prompt_tokens > 128000:
            cost *= 2
        return cost
    elif "gemini-2.0-flash-exp" in model.lower():
        # price unknown for gemini-2.0-flash-exp, assuming same price as gemini-1.5-flash
        cost = 0.000000075 * prompt_tokens + 0.0000003 * completion_tokens
        if prompt_tokens > 128000:
            cost *= 2
        return cost
    elif "gemini-2.5-pro-preview-05-06" in model.lower():
        # https://ai.google.dev/gemini-api/docs/pricing#gemini-2.5-pro-preview, accessed 05/08/2025
        cost = (0.00000125 if prompt_tokens <= 200000 else 0.0000025) * prompt_tokens
        cost += (0.00001 if prompt_tokens <= 200000 else 0.000015) * completion_tokens
        return cost
    elif "qwen2-72b" in model.lower():
        # assuming hosted on Together
        # https://www.together.ai/pricing, accessed 12/11/2024
        return 0.0000009 * (prompt_tokens + completion_tokens)
    elif "qwen2p5-72b" in model.lower():
        # assuming hosted on Together
        # https://www.together.ai/pricing, accessed 12/14/2024
        return 0.0000012 * (prompt_tokens + completion_tokens)
    elif "llama-v3p1-405b-instruct" in model.lower():
        # assuming hosted on Fireworks AI
        # https://fireworks.ai/pricing, accessed 12/11/2024
        return 0.000003 * (prompt_tokens + completion_tokens)
    elif "llama-v3p1-70b-instruct" in model.lower():
        # assuming hosted on Fireworks AI
        return 0.0000009 * (prompt_tokens + completion_tokens)
    elif "llama-v3p3-70b-instruct" in model.lower():
        # assuming hosted on Fireworks AI
        return 0.0000009 * (prompt_tokens + completion_tokens)
    elif "amazon.nova-pro-v1:0" in model.lower():
        # assuming hosted on Amazon Bedrock
        # https://aws.amazon.com/bedrock/pricing/, accessed 12/11/2024
        return 0.0000008 * prompt_tokens + 0.0000032 * completion_tokens
    else:
        raise ValueError(f"Unknown model: {model}")

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


def analyze_traj_json_file(filepath: str) -> int:
    """
    Analyze a single trajectory JSON file and extract the rounds.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
        return len(data)


def analyze_cost_json_file(filepath: str) -> float:
    """
    Analyze a single cost JSON file and extract the cost.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
        return calculate_cost('gpt-4o', data['prompt_token_count'], data['completion_token_count'])


def analyze_folder(folder_path: str) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, float]]]:
    """
    Analyze all eval_*.json & traj_*.json files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing JSON files
        
    Returns:
        dictionaries:
        - eval_results: Dictionary with task as key and (total, result) tuple as value
        - traj_results: Dictionary with task as key and rounds as value
        - cost_results: Dictionary with task as key and cost as value
    """
    eval_results = {}
    traj_results = {}
    cost_results = {}

    # include all files in the nested folders
    eval_pattern = os.path.join(folder_path, "**", "eval_result.json")
    traj_pattern = os.path.join(folder_path, "**", "chat_history.json")
    cost_pattern = os.path.join(folder_path, "**", "token_count.json")
    
    for filepath in glob.glob(eval_pattern):
        total, result = analyze_eval_json_file(filepath)
        key = os.path.basename(os.path.dirname(filepath))
        eval_results[key] = (total, result)

    for filepath in glob.glob(traj_pattern):
        rounds = analyze_traj_json_file(filepath)
        key = os.path.basename(os.path.dirname(filepath))
        traj_results[key] = rounds

    for filepath in glob.glob(cost_pattern):
        cost = analyze_cost_json_file(filepath)
        key = os.path.basename(os.path.dirname(filepath))
        cost_results[key] = cost

    return eval_results, traj_results, cost_results

def get_task_nature_category(task_name: str) -> str:
    """
    Get the nature category of the task.
    """
    task_nature = task_name.split('-')[0]
    if task_nature.lower() in ['sde', 'pm', 'ds', 'admin', 'hr', 'finance']:
        return task_nature
    else:
        return "other"

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
    # check if the current directory and 'workspaces' directory are in the same parent directory
    # this is because we need to access each task's dependencies.yml file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    workspaces_dir = os.path.join(os.path.dirname(parent_dir), 'workspaces')
    if not os.path.exists(workspaces_dir):
        print("Error: 'workspaces' directory not found in the grandparent directory")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: python summarise_results.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory")
        sys.exit(1)
    
    eval_results, traj_results, cost_results = analyze_folder(folder_path)
    
    if not eval_results:
        print(f"No eval_*.json files found in {folder_path}")
        return

    # load all dependencies.yml files
    # iterate over workspaces/tasks/*/dependencies.yml and load the yaml file
    service_to_tasks = {}
    for task_image_name in eval_results.keys():
        # trim the trailing "-image"
        task_name = task_image_name.replace("-image", "")
        dependencies_file = os.path.join(workspaces_dir, 'tasks', task_name, 'dependencies.yml')
        with open(dependencies_file, 'r') as f:
            dependencies = yaml.safe_load(f)
            for service in dependencies or []:
                if service not in service_to_tasks:
                    service_to_tasks[service] = []
                service_to_tasks[service].append(task_image_name)

    # Create list of results with completion ratios for sorting
    detailed_results = [
        (
            task_name,
            total,
            result,
            calculate_score(total, result),
            is_perfect_completion(total, result),
            get_task_nature_category(task_name)
        )
        for task_name, (total, result) in eval_results.items()
    ]
    
    # Sort by score in descending order
    detailed_results.sort(key=lambda x: (-x[3], x[0]))
    
    # Calculate perfect completion stats
    perfect_completions = sum(1 for _, _, _, _, is_perfect, _ in detailed_results if is_perfect)
    
    # Print header
    print("\n# Evaluation Results Report")
    print("\n## Results per File")
    print("\n*Sorted by score (⭐ indicates perfect completion)*\n")
    
    # Print table header
    print("| Filename | Total | Result | Score | rounds | Cost |")
    print("|----------|--------|---------|-------|-------|------|")
    
    # Print individual file results
    for task_name, total, result, score, is_perfect, task_nature in detailed_results:
        perfect_marker = " ⭐" if is_perfect else ""
        if task_name in traj_results:
            traj_result = traj_results[task_name]
        else:
            print(f"WARNING: {task_name} not found in traj_results")
            traj_result = 0
        if task_name in cost_results:
            cost_result = cost_results[task_name]
        else:
            print(f"WARNING: {task_name} not found in cost_results")
            cost_result = 0
        print(f"| {task_name} | {total:,} | {result:,} | {score:.2f}{perfect_marker} | {traj_result} | {cost_result:.2f} |")
    
    # Print summary section
    print("\n## Summary\n")
    print(f"**Tasks Evaluated:** {len(eval_results)}\n")
    print(f"**Perfect Completions:** {perfect_completions}/{len(eval_results)} ({(perfect_completions/len(eval_results)*100):.2f}%)\n")
    
    overall_score = sum(score for _, _, _, score, _, _ in detailed_results) / len(detailed_results) * 100
    avg_rounds = sum(rounds for rounds in traj_results.values()) / len(traj_results)
    avg_cost = sum(cost for cost in cost_results.values()) / len(cost_results)
    print(f"**Overall Score:** {overall_score:.2f}%\n")
    print(f"**Average rounds:** {avg_rounds:.2f}\n")
    print(f"**Average Cost (USD):** {avg_cost:.2f}\n")

    # Additional statistics
    if detailed_results:
        highest_score = max(score for _, _, _, score, _, _ in detailed_results)
        lowest_score = min(score for _, _, _, score, _, _ in detailed_results)
        median_score = detailed_results[len(detailed_results) // 2][3]
        avg_score = sum(score for _, _, _, score, _, _ in detailed_results) / len(detailed_results)
        
        print("\n## Statistics\n")
        print("| Metric | Value |")
        print("|---------|--------|")
        print(f"| Highest Task Score | {highest_score*100:.2f}% |")
        print(f"| Lowest Task Score | {lowest_score*100:.2f}% |")
        print(f"| Median Task Score | {median_score*100:.2f}% |")
        print(f"| Average Task Score | {avg_score*100:.2f}% |")

        # compute avg score per nature category
        print("\n## Statistics per Nature Category\n")
        print("| Metric | Value |")
        print("|---------|--------|")
        for task_nature in ['sde', 'pm', 'ds', 'admin', 'hr', 'finance', 'other']:
            num_of_tasks = sum(1 for _, _, _, _, _, nature_category in detailed_results if nature_category == task_nature)
            task_nature_score = 0 if num_of_tasks == 0 else sum(score for _, _, _, score, _, nature_category in detailed_results if nature_category == task_nature) / num_of_tasks
            perfect_completions = sum(1 for _, _, _, _, is_perfect, nature_category in detailed_results if nature_category == task_nature and is_perfect)
            perfect_completions_ratio = 0 if num_of_tasks == 0 else perfect_completions / num_of_tasks
            print(f"| Perfect Completions for {task_nature} | {perfect_completions} ({perfect_completions_ratio*100:.2f}%) |")
            print(f"| Average Score for {task_nature} | {task_nature_score*100:.2f}% |")

        # compute avg score per service category
        print("\n## Statistics per Service Category\n")
        print("| Metric | Value |")
        print("|---------|--------|")
        for service_category in ['gitlab', 'plane', 'rocketchat', 'owncloud']:
            num_of_tasks = len(service_to_tasks.get(service_category, []))
            service_category_score = 0 if num_of_tasks == 0 else sum(score for task_name, _, _, score, _, _ in detailed_results if task_name in service_to_tasks[service_category]) / num_of_tasks
            perfect_completions = sum(1 for task_name, _, _, _, is_perfect, _ in detailed_results if task_name in service_to_tasks.get(service_category, []) and is_perfect)
            perfect_completions_ratio = 0 if num_of_tasks == 0 else perfect_completions / num_of_tasks
            print(f"| Perfect Completions for {service_category} | {perfect_completions} ({perfect_completions_ratio*100:.2f}%) |")
            print(f"| Average Score for {service_category} | {service_category_score*100:.2f}% |")

if __name__ == "__main__":
    main()