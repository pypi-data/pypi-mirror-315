from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTabBar, QToolBar, QSlider, QMenu, QSpinBox, QAbstractSlider

from .container import WidgetMix, Qt
from ..gui import Action


class TabBar(WidgetMix, QTabBar):
    def __init__(self,
                 tabs: list[dict] = None,
                 current_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if current_changed: self.currentChanged.connect(current_changed)
        for x in tabs or {}:
            if icon := x.get('icon', None):
                self.addTab(icon, x['label'])
                continue
            self.addTab(x['label'])


class ToolBar(WidgetMix, QToolBar):
    def __init__(self, title='', *,
                 icon_size: int | tuple[int, int] = None,
                 triggered: Callable[[Action], None] = None,
                 **kwargs
                 ):
        if isinstance(icon_size, int):
            icon_size = (icon_size, icon_size)
        super().__init__(title, **kwargs)

        if triggered: self.actionTriggered.connect(triggered)
        if icon_size is not None:
            self.setIconSize(QSize(*icon_size))


class AbsSliderMix(WidgetMix):
    ...


class QAsSlider(AbsSliderMix, QAbstractSlider):
    ...


class Slider(AbsSliderMix, QSlider):
    def __init__(self,
                 value=0,
                 maximum=100, *,
                 minimum=0,
                 axis=Qt.Orientation.Hor,
                 value_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(axis, **kwargs)
        if value_changed: self.valueChanged.connect(value_changed)
        self.setRange(minimum, maximum)
        self.setValue(int(value))


class Menu(WidgetMix, QMenu):
    def __init__(self, *actions: QAction,
                 title='',
                 triggered=Callable[[QAction], None],
                 **kwargs
                 ):
        super().__init__(title, **kwargs)
        if triggered: self.triggered.connect(triggered)
        self.addActions(*actions)


class AbsSpinBoxMix(WidgetMix):
    ...


class AbsSpinBox(AbsSpinBoxMix, QAbstractSlider):
    ...


class SpinBox(AbsSpinBoxMix, QSpinBox):
    def __init__(self, value=0,
                 maximum=99, *,
                 minimum=0,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setRange(minimum, maximum)
        self.setValue(value)
