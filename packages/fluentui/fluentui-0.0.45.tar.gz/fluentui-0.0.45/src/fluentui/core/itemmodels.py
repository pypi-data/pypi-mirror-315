from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, QAbstractTableModel, \
    QSortFilterProxyModel, QObject

ModelIndex: type[QModelIndex | QPersistentModelIndex] = QModelIndex | QPersistentModelIndex


class AbsItemModelMix:
    def index(self, row: int | ModelIndex, column: int = None, parent=QModelIndex()) -> QModelIndex:
        if isinstance(row, QModelIndex):
            column = row.column() if column is None else column
            row = row.row()
        return super().index(row, column or 0, parent)

    def hasIndex(self, row: int, column=0, parent=QModelIndex()) -> bool:
        return super().hasIndex(row, column, parent)


class AbsItemModel(AbsItemModelMix, QAbstractItemModel):
    ...


class AbsProxyModelMix(AbsItemModelMix):
    ...


class AbsProxyModel(AbsProxyModelMix):
    ...


class SortFilterProxyModel(AbsProxyModelMix, QSortFilterProxyModel):
    def __init__(self, source: QAbstractItemModel = None, parent: QObject = None):
        super().__init__(parent)
        if source is not None:
            self.setSourceModel(source)


class AbsTableModelMix(AbsItemModelMix):
    ...


class AbsTableModel(AbsTableModelMix, QAbstractTableModel):
    ...
