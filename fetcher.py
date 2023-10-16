import csv


def read_csv_data(csv_path):
    data = {'negative': [], 'positive': []}
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data[row[2]].append(row[0])
    return data


def create_generator(data, class_name):
    for item in data[class_name]:
        yield item
    yield None


def get_next_item(csv_path, class_name):
    data = read_csv_data(csv_path)
    return create_generator(data, class_name)


negative_generator = get_next_item("annotation.csv", "negative")

while True:
    file_path = next(negative_generator)
    if file_path is None:
        break
    print(file_path)
