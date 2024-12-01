import json
import glob
import os
import sys
from typing import Dict, Tuple

def analyze_json_file(filepath: str) -> Tuple[int, int]:
    """
    Analyze a single JSON file and extract the total and result from final_score.
    
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

def analyze_folder(folder_path: str) -> Dict[str, Tuple[int, int]]:
    """
    Analyze all eval_*.json files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing JSON files
        
    Returns:
        Dictionary with filename as key and (total, result) tuple as value
    """
    results = {}
    pattern = os.path.join(folder_path, "eval_*.json")
    
    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        total, result = analyze_json_file(filepath)
        results[filename] = (total, result)
    
    return results

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
    
    results = analyze_folder(folder_path)
    
    if not results:
        print(f"No eval_*.json files found in {folder_path}")
        return
    
    # Calculate totals and create sorted results with completion ratios
    total_sum = sum(total for total, _ in results.values())
    result_sum = sum(result for _, result in results.values())
    
    # Create list of results with completion ratios for sorting
    detailed_results = [
        (
            filename,
            total,
            result,
            calculate_score(total, result),
            is_perfect_completion(total, result)
        )
        for filename, (total, result) in results.items()
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
    print("| Filename | Total | Result | Score |")
    print("|----------|--------|---------|-------|")
    
    # Print individual file results
    for filename, total, result, score, is_perfect in detailed_results:
        perfect_marker = " ⭐" if is_perfect else ""
        print(f"| {filename} | {total:,} | {result:,} | {score:.2f}{perfect_marker} |")
    
    # Print summary section
    print("\n## Summary\n")
    print(f"**Tasks Evaluated:** {len(results)}\n")
    print(f"**Perfect Completions:** {perfect_completions}/{len(results)} ({(perfect_completions/len(results)*100):.1f}%)\n")
    
    overall_score = sum(score for _, _, _, score, _ in detailed_results) / len(detailed_results) * 100
    print(f"**Overall Score:** {overall_score:.2f}%")
    
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