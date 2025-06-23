from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QFileDialog, QMessageBox, QProgressBar
)
from PySide6.QtCore import QThread, Signal
import sys
import os
import time
from converter import convert_audio, Format_audio


class AudioConverterThread(QThread):

    progress_updated = Signal(int)

    conversion_finished = Signal(bool, str)

    def __init__(self, input_file, output_path, format_out, kwargs):
        super().__init__()
        self.input_file = input_file
        self.output_path = output_path
        self.format_out = format_out
        self.kwargs = kwargs

    def run(self):
        try:

            for i in range(101):
                time.sleep(0.05)
                self.progress_updated.emit(i)


            convert_audio(self.input_file, self.output_path, self.format_out, **self.kwargs)
            self.conversion_finished.emit(True, f"Plik zapisany jako:\n{self.output_path}")

        except Exception as e:
            self.conversion_finished.emit(False, str(e))



class AudioConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Converter")
        self.resize(400, 300)
        self.input_file = None
        self.output_dir = "audio_samples"
        self.converter_thread = None
        self.setup_ui()


        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label_file = QLabel("Brak pliku")
        self.btn_choose_file = QPushButton("Wybierz plik")
        self.btn_choose_file.clicked.connect(self.choose_file)

        self.combo_format = QComboBox()
        self.combo_format.addItems(Format_audio)

        self.input_sample_rate = QLineEdit()
        self.input_sample_rate.setPlaceholderText("Sample rate (np. 44100)")

        self.input_bit_depth = QLineEdit()
        self.input_bit_depth.setPlaceholderText("Bit depth (np. 16)")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.btn_convert = QPushButton("Konwertuj")
        self.btn_convert.clicked.connect(self.convert_file)

        layout.addWidget(self.label_file)
        layout.addWidget(self.btn_choose_file)
        layout.addWidget(QLabel("Format docelowy:"))
        layout.addWidget(self.combo_format)
        layout.addWidget(self.input_sample_rate)
        layout.addWidget(self.input_bit_depth)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.btn_convert)

        self.setLayout(layout)

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wybierz plik audio","", "Pliki audio (*.mp3 *.wav *.m4a *.flac *.ogg *.amr)")
        if file:
            self.input_file = file
            self.label_file.setText(f"Plik: {os.path.basename(file)}")
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(False)

    def convert_file(self):
        if not self.input_file:
            QMessageBox.warning(self, "Błąd", "Nie wybrano pliku!")
            return

        format_out = self.combo_format.currentText()
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        output_path = os.path.join(self.output_dir, f"{base_name}_converted.{format_out}")

        kwargs = {}
        if format_out == "wav":
            if self.input_sample_rate.text():
                kwargs['sample_rate'] = self.input_sample_rate.text()
            if self.input_bit_depth.text():
                kwargs['bit_depth'] = self.input_bit_depth.text()


        self.btn_convert.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)


        self.converter_thread = AudioConverterThread(
            self.input_file, output_path, format_out, kwargs
        )
        self.converter_thread.progress_updated.connect(self.update_progress_bar)
        self.converter_thread.conversion_finished.connect(self.conversion_finished)
        self.converter_thread.start() # Rozpocznij wątek

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self, success, message):

        self.btn_convert.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

        if success:
            QMessageBox.information(self, "Sukces", message)
        else:
            QMessageBox.critical(self, "Błąd", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioConverterGUI()
    window.show()
    sys.exit(app.exec())