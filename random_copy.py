import random
import os
import shutil


def randomize_and_copy(dataset_path, destination_path):
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    all_files = []

    for class_name in ["negative", "positive"]:
        class_path = os.path.join(dataset_path, class_name)
        files_in_class = os.listdir(class_path)
        sorted_files = sorted(files_in_class)

        for file_name in sorted_files:
            full_path = os.path.join(class_path, file_name)
            all_files.append(full_path)

    used_names = set()
    for file_path in all_files:
        new_file_name = f"{random.randint(0, 9999):04d}.txt"
        while new_file_name in used_names:
            new_file_name = f"{random.randint(0, 9999):04d}.txt"
        used_names.add(new_file_name)
        shutil.copy(file_path, os.path.join(destination_path, new_file_name))


randomize_and_copy("dataset", "randomized_dataset")
