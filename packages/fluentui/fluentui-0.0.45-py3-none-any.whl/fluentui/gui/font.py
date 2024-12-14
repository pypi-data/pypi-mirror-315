from PySide6.QtGui import QFontDatabase, QFont


class FontDatabase(QFontDatabase):
    @classmethod
    def applicationFontFamilies(cls, fileNames: list[str]) -> list[str]:
        return [super().applicationFontFamilies(y) for
                y in [cls.addApplicationFont(x) for x in fileNames]]


class Font(QFont):
    def __init__(self,
                 families='Segoe UI, Microsoft YaHei UI, PingFang SC', *,
                 pixel=0,
                 point=0,
                 weight=QFont.Weight.Normal,
                 italic=False,
                 ):
        super().__init__([x.strip() for x in families.split(',')], -1, weight, italic)
        if pixel > 0: self.setPixelSize(pixel)
        if point > 0: self.setPointSize(point)
