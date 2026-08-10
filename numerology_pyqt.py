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


class NumerologyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.model = NumerologyModel()
        self.setWindowTitle("Numeralogy")
        self.resize(760, 320)

        self.name_edit = QtWidgets.QLineEdit("Manian")
        self.total_edit = QtWidgets.QLineEdit()
        self.total_edit.setReadOnly(True)
        self.term_total_edit = QtWidgets.QLineEdit()
        self.term_total_edit.setReadOnly(True)
        self.desired_spin = QtWidgets.QSpinBox()
        self.desired_spin.setRange(1, 1000)
        self.desired_spin.setValue(20)
        self.max_length_spin = QtWidgets.QSpinBox()
        self.max_length_spin.setRange(1, 100)
        self.max_length_spin.setValue(6)
        self.generated_edit = QtWidgets.QLineEdit()
        self.generated_edit.setReadOnly(True)

        self.export_button = QtWidgets.QPushButton("Export Names")
        self.export_button.clicked.connect(self.export_names)

        self.name_edit.textChanged.connect(self.update_totals)
        self.update_totals()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel("Registration Name:\nName Prefix For Export:"), 0, 0)
        layout.addWidget(self.name_edit, 0, 1, 1, 3)

        layout.addWidget(QtWidgets.QLabel("Name Sum:"), 1, 2)
        layout.addWidget(self.total_edit, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Name Recursive Sum:"), 2, 2)
        layout.addWidget(self.term_total_edit, 2, 3)

        layout.addWidget(QtWidgets.QLabel("Desired Number:"), 3, 0)
        layout.addWidget(self.desired_spin, 3, 1)
        layout.addWidget(self.export_button, 3, 2)
        layout.addWidget(QtWidgets.QLabel("Max Length:"), 4, 0)
        layout.addWidget(self.max_length_spin, 4, 1)
        layout.addWidget(QtWidgets.QLabel("Generated Name:"), 5, 0)
        layout.addWidget(self.generated_edit, 5, 1, 1, 3)

    def update_totals(self):
        name = self.name_edit.text().strip()
        total = self.model.find_sum(name)
        self.total_edit.setText(str(total))
        self.term_total_edit.setText(str(self.model.find_term_sum(total)))

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
