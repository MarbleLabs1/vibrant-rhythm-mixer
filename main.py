
import sys
from PyQt6.QtWidgets import QApplication
from dj_pad import DJPadApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DJPadApp()
    window.show()
    sys.exit(app.exec())
