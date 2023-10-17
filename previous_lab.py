import csv
import os
import shutil
import random


def create_annotation(dataset_path, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for class_name in ["negative", "positive"]:
            class_dir = os.path.join(dataset_path, class_name)
            for file_name in os.listdir(class_dir):
                abs_path = os.path.abspath(os.path.join(class_dir, file_name))

                # Получаем относительный путь
                full_path = os.path.join(class_dir, file_name)
                rel_path = os.path.relpath(full_path, dataset_path)

                csvwriter.writerow([abs_path, rel_path, class_name])


def copy_and_rename(dataset_path, dest_path, annotation_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    with open(annotation_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for class_name in ["negative", "positive"]:
            class_path = os.path.join(dataset_path, class_name)
            for file_name in sorted(os.listdir(class_path)):
                new_file_name = f"{class_name}_{file_name}"
                dest_file_path = os.path.join(dest_path, new_file_name)
                shutil.copy(os.path.join(class_path, file_name), dest_file_path)

                abs_path = os.path.abspath(dest_file_path)
                rel_path = os.path.relpath(dest_file_path, dataset_path)

                csvwriter.writerow([abs_path, rel_path, class_name])


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


def get_next_file(dataset_path, class_name):
    class_dir = os.path.join(dataset_path, class_name)
    files = sorted(os.listdir(class_dir))

    for file_name in files:
        yield os.path.join(class_dir, file_name)
    yield None
