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
    
    # Calculate totals
    total_sum = sum(total for total, _ in results.values())
    result_sum = sum(result for _, result in results.values())
    
    # Find the longest filename for proper formatting
    max_filename_length = max(len(filename) for filename in results.keys())
    column_width = max(max_filename_length, 70)  # minimum 70 characters for readability
    
    # Print individual file results
    print("\nResults per file:")
    print("-" * (column_width + 25))  # Adjust line length based on filename length
    print(f"{'Filename':<{column_width}} {'Total':>10} {'Result':>10}")
    print("-" * (column_width + 25))
    
    for filename, (total, result) in sorted(results.items()):
        print(f"{filename:<{column_width}} {total:>10} {result:>10}")
    
    # Print summary
    print("\nSummary:")
    print("-" * (column_width + 25))
    print(f"Number of tasks evaluated: {len(results)}")
    print(f"Sum of total points: {total_sum}")
    print(f"Sum of actual points: {result_sum}")
    print(f"Overall score: {(result_sum / total_sum * 100):.2f}%" if total_sum > 0 else "N/A")

if __name__ == "__main__":
    main()