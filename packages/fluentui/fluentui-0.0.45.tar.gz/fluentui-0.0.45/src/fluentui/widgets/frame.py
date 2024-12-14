from PySide6.QtWidgets import QWidget, QToolBox, QStackedWidget, QFrame, QScrollArea, QSplitter, QLabel

from .container import WidgetMix, Qt


class FrameMix(WidgetMix):
    def __init__(self,
                 frame_shape: QFrame.Shape = None,
                 line_width: int = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if frame_shape is not None: self.setFrameShape(frame_shape)
        if line_width is not None: self.setLineWidth(line_width)


class Frame(FrameMix, QFrame):
    ...


class Label(FrameMix, QLabel):
    def __init__(self,
                 text='',
                 align: Qt.AlignmentFlag = None,
                 word_wrap=False,
                 interaction_flag: Qt.TextInteraction = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setText(text)
        if interaction_flag is not None: self.setTextInteractionFlags(interaction_flag)
        if align is not None: self.setAlignment(align)
        self.setWordWrap(word_wrap)


class Line(FrameMix, QLabel):
    def __init__(self, orient='hor', thick=1, **kwargs):
        key = 'height' if orient == 'hor' else 'width'
        super().__init__(**kwargs | {key: thick})


class Horline(Line):
    def __init__(self, thick=1, **kwargs):
        super().__init__(orient='hor', thick=thick, **kwargs)


class Verline(Line):
    def __init__(self, thick=1, **kwargs):
        super().__init__(orient='ver', thick=thick, **kwargs)


class AbsScrollAreaMix(FrameMix):
    def __init__(self,
                 hor_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 ver_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 **kwargs):
        super().__init__(**kwargs)
        if hor_scroll_bar_policy is not None:
            self.setHorizontalScrollBarPolicy(hor_scroll_bar_policy)
        if ver_scroll_bar_policy is not None:
            self.setVerticalScrollBarPolicy(ver_scroll_bar_policy)


class ScrollArea(AbsScrollAreaMix, QScrollArea):
    ...


class ToolBox(FrameMix, QToolBox):
    def __init__(self, *children: dict, **kwargs):
        super().__init__(**kwargs)
        for x in children:
            if icon := x.get('icon'):
                self.addItem(x['widget'], icon, x['text'])
                continue
            self.addItem(x['widget'], x['text'])


class Splitter(FrameMix, QSplitter):
    def __init__(self, *children: QWidget,
                 sizes: list[int] = None,
                 handle_width=5,
                 children_collapsible=True,
                 orient=Qt.Orientation.Hor,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setOrientation(orient)
        self.setHandleWidth(handle_width)
        self.setChildrenCollapsible(children_collapsible)
        for x in children or []: self.addWidget(x)
        if sizes: self.setSizes(sizes or [])


class StackedView(FrameMix, QStackedWidget):
    def __init__(self, *stack: QWidget, **kwargs):
        super().__init__(**kwargs)
        for x in stack or ():
            self.addWidget(x)
