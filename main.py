import sys
import base64
import zlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
import qrcode
from PIL.ImageQt import ImageQt


class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 400, 500)

        # Layout principale
        layout = QVBoxLayout()

        # Pulsante per caricare il file
        self.file_button = QPushButton("Carica File")
        self.file_button.clicked.connect(self.load_file)
        layout.addWidget(self.file_button)

        # Etichetta per mostrare il QR Code
        self.qr_label = QLabel("QR Code generato apparirà qui.")
        self.qr_label.setScaledContents(True)
        self.qr_label.setFixedSize(300, 300)
        layout.addWidget(self.qr_label)

        # Pulsante per salvare il QR Code
        self.save_button = QPushButton("Salva QR Codes")
        self.save_button.clicked.connect(self.save_all_qr_codes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.file_data = None
        self.qr_images = []

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona un file")
        if file_path:
            with open(file_path, "rb") as file:
                self.file_data = file.read()

            # Applica la compressione a cascata
            compressed_data = self.cascade_compress(self.file_data)

            # Suddividi i dati compressi in blocchi e genera i QR Code
            self.split_and_generate_qr_codes(compressed_data)

    def cascade_compress(self, data):
        """Applica fino a 5 compressioni successive usando zlib e una compressione finale."""
        for _ in range(5):
            data = zlib.compress(data, level=9)
        return self.base2048_encode(data)

    def base2048_encode(self, data):
        """Codifica i dati in una rappresentazione Base2048."""
        encoded = []
        for i in range(0, len(data), 2):
            # Prendi 2 byte e codificali in un unico valore
            if i + 1 < len(data):
                value = (data[i] << 8) + data[i + 1]
            else:
                value = data[i]
            encoded.append(value)
        return ''.join(chr(v) for v in encoded if v < 2048)

    def split_and_generate_qr_codes(self, data):
        """Suddivide i dati compressi in blocchi e genera i QR Code."""
        # Limite massimo per un QR Code di livello L e versione 40
        max_size = 2953  # byte
        self.qr_images = []

        # Dividi i dati in blocchi
        chunks = [data[i:i + max_size] for i in range(0, len(data), max_size)]

        for idx, chunk in enumerate(chunks):
            qr = qrcode.QRCode(
            version=40,  # Forza la versione massima (40)
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)

        try:
            qr.make(fit=False)  # Forza il fit per i blocchi definiti
            qr_image = qr.make_image(fill_color="black", back_color="white")
            self.qr_images.append(qr_image)
        except ValueError as e:
            QMessageBox.warning(
                self,
                "Errore",
                f"Impossibile generare il QR Code per il blocco {idx + 1}. Errore: {e}",
            )
        return

        if self.qr_images:
            # Mostra il primo QR Code generato nella UI
            qt_image = ImageQt(self.qr_images[0])
            pixmap = QPixmap.fromImage(qt_image)
            self.qr_label.setPixmap(pixmap)


    def save_all_qr_codes(self):
        """Salva tutti i QR Code generati e li combina in un'unica immagine."""
        if not self.qr_images:
            QMessageBox.warning(self, "Errore", "Nessun QR Code generato!")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "Seleziona una cartella per salvare i QR Codes")
        if not output_folder:
            return

        # Salva ogni QR Code come immagine PNG
        file_paths = []
        for idx, qr_image in enumerate(self.qr_images):
            file_path = f"{output_folder}/qr_code_part_{idx + 1}.png"
            qr_image.save(file_path)
            file_paths.append(file_path)

        # Combina i QR Codes in un'unica immagine
        self.combine_qr_codes(file_paths, output_folder)

    def combine_qr_codes(self, file_paths, output_folder):
        """Combina le immagini QR salvate in un unico file PNG."""
        images = [Image.open(fp) for fp in file_paths]

        # Calcola dimensioni della griglia
        grid_size = int(len(images) ** 0.5) + 1
        qr_width, qr_height = images[0].size
        combined_width = grid_size * qr_width
        combined_height = grid_size * qr_height

        # Crea una nuova immagine vuota per la griglia
        combined_image = Image.new("RGB", (combined_width, combined_height), "white")
        draw = ImageDraw.Draw(combined_image)

        for idx, image in enumerate(images):
            x = (idx % grid_size) * qr_width
            y = (idx // grid_size) * qr_height
            combined_image.paste(image, (x, y))

        # Salva l'immagine combinata
        combined_path = f"{output_folder}/combined_qr_codes.png"
        combined_image.save(combined_path)
        QMessageBox.information(self, "Salvataggio Completato", f"QR Codes combinati salvati in: {combined_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
