from PySide6.QtGui import QPixmap, QIconEngine, QIcon, QImage


class Icon(QIcon):
    def __init__(self, icon: str | QPixmap | QIconEngine | QIcon | QImage = None):
        if icon is None:
            super().__init__()
        else:
            super().__init__(icon)
