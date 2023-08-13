import os
import glob

def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def count_lines_in_directory(directory):
    total_lines = 0
    for py_file in glob.glob(os.path.join(directory, '**/*.py'), recursive=True):
        total_lines += count_lines_in_file(py_file)
    return total_lines

def main(root_directory):
    total_lines = count_lines_in_directory(root_directory)
    print(f"Total lines in all .py files: {total_lines}")

if __name__ == "__main__":
    root_directory = "."  # Change this to the desired root directory
    main(root_directory)
