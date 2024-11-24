import yaml
import sys
import os

def validate_dependencies(file_path):
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
            if data is None:
                # empty yaml file
                return True
            if not isinstance(data, list):
                print(f'Error: {file_path} is not a valid array')
                return False
            if len(data) != len(set(data)):
                print(f'Error: {file_path} contains duplicate values')
                return False
            valid_deps = {'gitlab', 'rocketchat', 'plane', 'owncloud'}
            for dep in data:
                if dep.lower() not in valid_deps:
                    print(f'Error: Invalid dependency {dep} in {file_path}')
                    return False
        except yaml.YAMLError:
            print(f'Error: {file_path} is not a valid YAML file')
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_dependencies.py <path_to_dependencies.yml>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    if validate_dependencies(file_path):
        print(f"Dependencies in {file_path} are valid")
        sys.exit(0)
    else:
        sys.exit(1)