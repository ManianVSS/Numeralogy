import getpass
import sys
from pathlib import Path

from PyQt5 import QtWidgets


class NumerologyModel:
    def __init__(self):
        self.char_map = {
            " ": 0,
            "\t": 0,
            "\n": 0,
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 8,
            "g": 3,
            "h": 5,
            "i": 1,
            "j": 1,
            "k": 2,
            "l": 3,
            "m": 4,
            "n": 5,
            "o": 7,
            "p": 8,
            "q": 1,
            "r": 2,
            "s": 3,
            "t": 4,
            "u": 6,
            "v": 6,
            "w": 6,
            "x": 5,
            "y": 1,
            "z": 7,
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 8,
            "G": 3,
            "H": 5,
            "I": 1,
            "J": 1,
            "K": 2,
            "L": 3,
            "M": 4,
            "N": 5,
            "O": 7,
            "P": 8,
            "Q": 1,
            "R": 2,
            "S": 3,
            "T": 4,
            "U": 6,
            "V": 6,
            "W": 6,
            "X": 5,
            "Y": 1,
            "Z": 7,
        }
        self.vowel_array = "aeiou"

    def is_vowel(self, char):
        return char in self.vowel_array

    def find_sum(self, name):
        return sum(self.char_map.get(char, 0) for char in name)

    def digit_sum(self, number):
        return sum(int(digit) for digit in str(number))

    def find_term_sum(self, name_sum):
        while name_sum > 9:
            name_sum = self.digit_sum(name_sum)
        return name_sum

    def _export_name_tree(self, maxlength, desired_sum, callback, tree_parent_name_part=""):
        if maxlength <= 0:
            return

        parent_last_char = tree_parent_name_part[-1] if tree_parent_name_part else ""

        for iter_char in "abcdefghijklmnopqrstuvwxyz":
            if tree_parent_name_part.endswith(iter_char):
                continue

            if self.is_vowel(iter_char) and self.is_vowel(parent_last_char):
                continue

            iter_name = tree_parent_name_part + iter_char
            letter_value = self.char_map.get(iter_char, 0)

            if letter_value >= desired_sum:
                if letter_value == desired_sum:
                    callback(iter_name)
                continue

            self._export_name_tree(maxlength - 1, desired_sum - letter_value, callback, iter_name)

    def generate_names(self, prefix="", max_length=0, desired_sum=0):
        if max_length <= 0:
            return []

        prefix_sum = self.find_sum(prefix)
        if desired_sum <= prefix_sum:
            return []

        names = []
        remaining_length = max_length - len(prefix)
        self._export_name_tree(
            remaining_length,
            desired_sum - prefix_sum,
            names.append,
            prefix,
        )
        return names


class NumerologyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = NumerologyModel()
        self.dictionary_names = []
        self.default_initial = getpass.getuser()[:1].upper() if getpass.getuser() else ""

        self.setWindowTitle("Numeralogy")
        self.resize(960, 520)

        self.name_edit = QtWidgets.QLineEdit("Manian")
        self.total_without_initial_edit = QtWidgets.QLineEdit()
        self.total_without_initial_edit.setReadOnly(True)
        self.total_with_initial_edit = QtWidgets.QLineEdit()
        self.total_with_initial_edit.setReadOnly(True)
        self.term_without_initial_edit = QtWidgets.QLineEdit()
        self.term_without_initial_edit.setReadOnly(True)
        self.term_with_initial_edit = QtWidgets.QLineEdit()
        self.term_with_initial_edit.setReadOnly(True)
        self.desired_spin = QtWidgets.QSpinBox()
        self.desired_spin.setRange(1, 1000)
        self.desired_spin.setValue(20)
        self.max_length_spin = QtWidgets.QSpinBox()
        self.max_length_spin.setRange(1, 100)
        self.max_length_spin.setValue(6)
        self.generated_edit = QtWidgets.QLineEdit()
        self.generated_edit.setReadOnly(True)

        self.starts_with_edit = QtWidgets.QLineEdit()
        self.initial_edit = QtWidgets.QLineEdit()
        self.initial_edit.setPlaceholderText(f"Auto from OS user: {self.default_initial}")
        self.name_sum_spin = QtWidgets.QSpinBox()
        self.name_sum_spin.setRange(0, 200)
        self.term_sum_spin = QtWidgets.QSpinBox()
        self.term_sum_spin.setRange(0, 9)
        self.search_button = QtWidgets.QPushButton("Search Dictionary")
        self.search_button.clicked.connect(self.search_dictionary)
        self.clear_button = QtWidgets.QPushButton("Clear Filters")
        self.clear_button.clicked.connect(self.clear_filters)
        self.dictionary_path_label = QtWidgets.QLabel("No dictionary loaded")

        self.results_table = QtWidgets.QTableWidget(0, 8)
        self.results_table.setHorizontalHeaderLabels([
            "Name",
            "Initial",
            "Last Name",
            "Sum (no initial)",
            "Recursive Sum (no initial)",
            "Sum",
            "Recursive Sum",
            "Full Name",
        ])
        self.results_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.results_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.results_table.horizontalHeader().setStretchLastSection(True)

        self.export_button = QtWidgets.QPushButton("Export Names")
        self.export_button.clicked.connect(self.export_names)

        self.name_edit.textChanged.connect(self.update_totals)
        self.update_totals()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QGridLayout(central_widget)
        layout.addWidget(QtWidgets.QLabel("Registration Name:\nName Prefix For Export:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Dictionary File:"), 1, 0)
        layout.addWidget(self.dictionary_path_label, 1, 1, 1, 3)

        layout.addWidget(QtWidgets.QLabel("Name Sum (without initial):"), 2, 0)
        layout.addWidget(self.total_without_initial_edit, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Name Sum (with initial):"), 2, 2)
        layout.addWidget(self.total_with_initial_edit, 2, 3)
        layout.addWidget(QtWidgets.QLabel("Recursive Sum (without initial):"), 3, 0)
        layout.addWidget(self.term_without_initial_edit, 3, 1)
        layout.addWidget(QtWidgets.QLabel("Recursive Sum (with initial):"), 3, 2)
        layout.addWidget(self.term_with_initial_edit, 3, 3)

        layout.addWidget(QtWidgets.QLabel("Desired Number:"), 4, 0)
        layout.addWidget(self.desired_spin, 4, 1)
        layout.addWidget(QtWidgets.QLabel("Max Length:"), 4, 2)
        layout.addWidget(self.max_length_spin, 4, 3)
        layout.addWidget(self.export_button, 5, 0, 1, 4)

        layout.addWidget(QtWidgets.QLabel("Filter: Starts with"), 6, 0)
        layout.addWidget(self.starts_with_edit, 6, 1)
        layout.addWidget(QtWidgets.QLabel("Filter: Initial (blank = first letter of user)"), 6, 2)
        layout.addWidget(self.initial_edit, 6, 3)

        layout.addWidget(QtWidgets.QLabel("Filter: Name sum (0 = any)"), 7, 0)
        layout.addWidget(self.name_sum_spin, 7, 1)
        layout.addWidget(QtWidgets.QLabel("Filter: Recursive sum (0 = any)"), 7, 2)
        layout.addWidget(self.term_sum_spin, 7, 3)
        layout.addWidget(self.search_button, 8, 0, 1, 2)
        layout.addWidget(self.clear_button, 8, 2, 1, 2)

        layout.addWidget(self.results_table, 9, 0, 1, 4)

        layout.addWidget(self.results_table, 9, 0, 1, 4)

        self.create_menu()

    def create_menu(self):
        file_menu = self.menuBar().addMenu("&File")

        open_action = QtWidgets.QAction("Open Dictionary...", self)
        open_action.triggered.connect(self.open_dictionary)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QtWidgets.QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_dictionary(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Dictionary", str(Path.cwd()), "Text Files (*.txt);;All Files (*)")
        if not file_name:
            return

        try:
            with open(file_name, encoding="utf-8") as handle:
                lines = [line.strip() for line in handle if line.strip()]
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Load Error", f"Could not open dictionary file:\n{exc}")
            return

        self.dictionary_names = lines
        self.dictionary_path_label.setText(file_name)
        self.search_dictionary()

    def clear_filters(self):
        self.starts_with_edit.clear()
        self.name_sum_spin.setValue(0)
        self.term_sum_spin.setValue(0)
        self.search_dictionary()

    def compute_initial(self, name):
        configured_initial = self.initial_edit.text().strip().upper()
        if configured_initial:
            return configured_initial[0]

        return self.default_initial

    def compute_last_name(self, name):
        parts = [part for part in name.split() if part]
        return parts[-1] if len(parts) > 1 else parts[0] if parts else ""

    def compute_full_name(self, name, initial):
        if not name:
            return ""
        return f"{name} {initial}" if initial else name

    def search_dictionary(self):
        if not self.dictionary_names:
            QtWidgets.QMessageBox.information(self, "No Dictionary", "Please open a dictionary file first.")
            return

        starts_with = self.starts_with_edit.text().strip().lower()
        desired_sum = self.name_sum_spin.value()
        desired_term = self.term_sum_spin.value()

        filtered = []
        for name in self.dictionary_names:
            normalized = name.strip()
            if not normalized:
                continue
            if starts_with and not normalized.lower().startswith(starts_with):
                continue

            initial = self.compute_initial(normalized)
            full_name = self.compute_full_name(normalized, initial)

            total_without_initial = self.model.find_sum(normalized)
            term_without_initial = self.model.find_term_sum(total_without_initial)
            total_with_initial = self.model.find_sum(full_name)
            term_with_initial = self.model.find_term_sum(total_with_initial)

            if desired_sum and total_with_initial != desired_sum:
                continue

            if desired_term and term_with_initial != desired_term:
                continue

            filtered.append((
                normalized,
                initial,
                self.compute_last_name(normalized),
                total_without_initial,
                term_without_initial,
                total_with_initial,
                term_with_initial,
                full_name,
            ))

        self.results_table.setRowCount(len(filtered))
        for row, (name, initial, last_name, total_without_initial, term_without_initial, total_with_initial, term_with_initial, full_name) in enumerate(filtered):
            self.results_table.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self.results_table.setItem(row, 1, QtWidgets.QTableWidgetItem(initial))
            self.results_table.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
            self.results_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(total_without_initial)))
            self.results_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(term_without_initial)))
            self.results_table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(total_with_initial)))
            self.results_table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(term_with_initial)))
            self.results_table.setItem(row, 7, QtWidgets.QTableWidgetItem(full_name))

    def update_totals(self):
        name = self.name_edit.text().strip()
        initial = self.compute_initial(name)
        total_without_initial = self.model.find_sum(name)
        term_without_initial = self.model.find_term_sum(total_without_initial)

        full_name = self.compute_full_name(name, initial)
        total_with_initial = self.model.find_sum(full_name)
        term_with_initial = self.model.find_term_sum(total_with_initial)

        self.total_without_initial_edit.setText(str(total_without_initial))
        self.term_without_initial_edit.setText(str(term_without_initial))
        self.total_with_initial_edit.setText(str(total_with_initial))
        self.term_with_initial_edit.setText(str(term_with_initial))

    def export_names(self):
        desired_sum = self.desired_spin.value()
        max_length = self.max_length_spin.value()
        prefix = self.name_edit.text().strip()

        if desired_sum <= 0 or max_length <= 0:
            QtWidgets.QMessageBox.warning(self, "Invalid input", "Please enter a positive desired value and length.")
            return

        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Names", str(Path.cwd() / "names.txt"), "Text Files (*.txt)")
        if not file_name:
            return

        names = self.model.generate_names(prefix=prefix, max_length=max_length, desired_sum=desired_sum)
        content = (
            f"Names for the combination Name Prefix: {prefix}, Desired sum: {desired_sum} "
            f"and Maximum Length: {max_length} is as follows.\n"
            + "\n".join(names)
        )
        Path(file_name).write_text(content, encoding="utf-8")
        self.generated_edit.setText(names[0] if names else "No matching names")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = NumerologyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
