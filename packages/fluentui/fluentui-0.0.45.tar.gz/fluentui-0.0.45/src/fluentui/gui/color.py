from PySide6.QtGui import QColor


class Color(QColor):
    def __init__(self, name='', alpha: float = 1):
        super().__init__(name)
        self.setAlphaF(alpha)
