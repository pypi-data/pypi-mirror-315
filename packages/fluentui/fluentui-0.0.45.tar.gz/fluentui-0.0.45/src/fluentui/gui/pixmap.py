from typing import Iterable

from PySide6.QtCore import Qt, QSize, QByteArray
from PySide6.QtGui import QPixmap


class Pixmap(QPixmap):
    def __init__(self,
                 size: int | tuple[int, int] | QSize = None,
                 filename='', format_: str = None, flags=Qt.ImageConversionFlag.AutoColor,
                 xpm: Iterable = None,
                 other: QPixmap = None,
                 ):
        """
        QPixmap()
        QPixmap(size)
        QPixmap(fileName, format=None, flags=Qt.AutoColor)
        QPixmap(xpm: Iterable)
        QPixmap(other: QPixmap)
        """
        if size is not None:
            if isinstance(size, tuple):
                size = QSize(size[0], size[1])
            elif isinstance(size, int):
                size = QSize(size, size)
            super().__init__(size)
        elif filename:
            super().__init__(filename, format_, flags)
        elif xpm:
            super().__init__(xpm)
        elif other is not None:
            super().__init__(other)
        else:
            super().__init__()

    @staticmethod
    def from_data(data: bytes | bytearray | QByteArray,
                  format_: str = None,
                  flags=Qt.ImageConversionFlag.AutoColor
                  ) -> 'Pixmap':
        pixmap = Pixmap()
        pixmap.loadFromData(data, format_, flags)
        return pixmap
