import re
import os
import csv

def read_cpp_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def extract_test_cases(content):
    # Regular expression to match the triple-quoted string and method definition
    pattern = re.compile(r"'''\s*(.*?)\s*'''\s*def\s*(.*?)\s*\(", re.DOTALL)
    
    test_cases = []
    
    for match in pattern.finditer(content):
        description = match.group(1).strip()
        method_name = match.group(2).strip()
        test_cases.append({
            'description': description,
            'method_name': method_name
        })

    return test_cases

def save_test_cases_to_csv(test_cases, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        cnt = 0
        for case in test_cases:
            cnt+=1
            id = str('GTECBLE_PYTHON_INTEGRATION_TEST_' + str(cnt))
            writer.writerow([id, case['method_name'], case['description']])


if __name__ == "__main__":
    python_file_path = os.path.join(os.path.dirname(__file__),'integrationtests.py')
    csv_file_path = os.path.join(os.path.dirname(__file__),'python_integration_tests.csv')
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    content = read_cpp_file(python_file_path)
    test_cases = extract_test_cases(content)
    save_test_cases_to_csv(test_cases, csv_file_path)