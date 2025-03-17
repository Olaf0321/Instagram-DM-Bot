import os
import csv

def add_path_to_csv(file_path, new_path):
    file_exists = os.path.exists(file_path)
    data = []
    
    if file_exists:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=' ')
            data = list(reader)
            if any(row["Path"] == new_path for row in data):
                return False

    new_no = int(data[-1]["No"]) + 1 if data else 1
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=' ')
        if not file_exists:
            writer.writerow(["No", "Path"])
        writer.writerow([new_no, new_path])
        print("correctly added path")
        return True