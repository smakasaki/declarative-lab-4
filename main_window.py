import os
import sys
from PyQt5 import QtWidgets
from previous_lab import copy_and_rename, create_annotation, get_next_file, randomize_and_copy


class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PD Lab 4 Griu")
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        self.folderpath = None
        self.positive_iter = None
        self.negative_iter = None

        self.layout = QtWidgets.QVBoxLayout()

        self.select_folder_btn = QtWidgets.QPushButton('Select Dataset Folder')
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_btn)

        self.create_annotation_btn = QtWidgets.QPushButton('Create Annotation File')
        self.create_annotation_btn.clicked.connect(self.create_annotation_file)
        self.layout.addWidget(self.create_annotation_btn)

        self.btn_copy_and_rename = QtWidgets.QPushButton("Copy and Rename", self)
        self.btn_copy_and_rename.clicked.connect(self.perform_copy_and_rename)
        self.layout.addWidget(self.btn_copy_and_rename)

        self.btn_randomize_and_copy = QtWidgets.QPushButton("Randomize and Copy", self)
        self.btn_randomize_and_copy.clicked.connect(self.perform_randomize_and_copy)
        self.layout.addWidget(self.btn_randomize_and_copy)

        self.next_positive_btn = QtWidgets.QPushButton('Next Positive Text')
        self.next_positive_btn.clicked.connect(self.show_next_positive)
        self.layout.addWidget(self.next_positive_btn)

        self.next_negative_btn = QtWidgets.QPushButton('Next Negative Text')
        self.next_negative_btn.clicked.connect(self.show_next_negative)
        self.layout.addWidget(self.next_negative_btn)

        self.text_display = QtWidgets.QPlainTextEdit()
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        self.setLayout(self.layout)

    def select_folder(self):
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

        if not selected_folder:
            QtWidgets.QMessageBox.warning(self, "Warning", "No folder selected.")
            return

        try:
            if not (os.path.exists(os.path.join(selected_folder, "positive")) and os.path.exists(
                    os.path.join(selected_folder, "negative"))):
                QtWidgets.QMessageBox.warning(self, "Warning",
                                              "The selected folder does not contain 'positive' and 'negative' subfolders.")
                return

            self.folderpath = selected_folder
            self.positive_iter = get_next_file(self.folderpath, "positive")
            self.negative_iter = get_next_file(self.folderpath, "negative")

            QtWidgets.QMessageBox.information(self, "Success", "Folder successfully selected!")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.folderpath = None
            self.positive_iter = None
            self.negative_iter = None

    def create_annotation_file(self):
        if not self.folderpath:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a dataset folder first.")
            return

        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Annotation File", "", "CSV Files (*.csv)")

        if save_path:
            try:
                create_annotation(self.folderpath, save_path)
                QtWidgets.QMessageBox.information(self, "Success", "Annotation file successfully created!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def perform_copy_and_rename(self):
        if not self.folderpath:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a dataset folder first.")
            return

        dest_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
        if not dest_path:
            return

        annotation_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Annotation File", "",
                                                                   "CSV Files (*.csv)")
        if not annotation_path:
            return

        try:
            copy_and_rename(self.folderpath, dest_path, annotation_path)
            QtWidgets.QMessageBox.information(self, "Success", "Files successfully copied and renamed!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def perform_randomize_and_copy(self):
        if not self.folderpath:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a dataset folder first.")
            return

        dest_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
        if not dest_path:
            return

        try:
            randomize_and_copy(self.folderpath, dest_path)
            QtWidgets.QMessageBox.information(self, "Success", "Files successfully randomized and copied!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def show_next_positive(self):
        try:
            if not self.folderpath:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please select a dataset folder first.")
                return

            next_file = next(self.positive_iter)
            if next_file:
                with open(next_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_display.setPlainText(content)
            else:
                self.text_display.setPlainText("No more positive texts.")
        except StopIteration:
            self.text_display.setPlainText("No more positive texts.")
        except Exception as e:
            self.text_display.setPlainText(f"An error occurred: {str(e)}")

    def show_next_negative(self):
        try:
            if not self.folderpath:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please select a dataset folder first.")
                return

            next_file = next(self.negative_iter)
            if next_file:
                with open(next_file, 'r', encoding='utf-8') as f:  # Указана кодировка 'cp1251'
                    content = f.read()
                    self.text_display.setPlainText(content)
            else:
                self.text_display.setPlainText("No more negative texts.")
        except StopIteration:
            self.text_display.setPlainText("No more negative texts.")
        except Exception as e:
            self.text_display.setPlainText(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
