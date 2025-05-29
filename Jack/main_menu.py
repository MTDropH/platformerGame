import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QLabel
)
from PyQt5.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Max the Knight - Main Menu")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        title = QLabel("Max the Knight")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        controls_button = QPushButton("Controls")
        controls_button.clicked.connect(self.show_controls)
        layout.addWidget(controls_button)

        self.setLayout(layout)

    def start_game(self):
        # Launch the Pygame game script
        self.close()
        subprocess.run([sys.executable, "maxtest.py"])

    def show_controls(self):
        QMessageBox.information(
            self,
            "Controls",
            "← / → : Move\n↑ / SPACE: Jump\nZ: Attack\nESC: Quit"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())