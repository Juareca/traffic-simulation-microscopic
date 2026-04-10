import sys
from PySide6.QtWidgets import QApplication

from presentacion.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # 🚀 SOLO CREAS LA VENTANA
    window = MainWindow(debug=True, seed=None)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()