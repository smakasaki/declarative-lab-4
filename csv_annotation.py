import csv
import os

def create_annotation(dataset_path, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for class_name in ["negative", "positive"]:
            class_dir = os.path.join(dataset_path, class_name)
            for file_name in os.listdir(class_dir):
                abs_path = os.path.abspath(os.path.join(class_dir, file_name))
                rel_path = os.path.join(dataset_path, class_name, file_name)
                csvwriter.writerow([abs_path, rel_path, class_name])

create_annotation("dataset/", "dataset_annot.csv")