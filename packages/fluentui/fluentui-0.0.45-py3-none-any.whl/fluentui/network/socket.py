from enum import Enum

from PySide6.QtCore import QByteArray
from PySide6.QtNetwork import QAbstractSocket
from PySide6.QtWebSockets import QWebSocket


class AbsSocketMix:
    class SocketState(Enum):
        Unconnected = QAbstractSocket.SocketState.UnconnectedState
        HostLookup = QAbstractSocket.SocketState.HostLookupState
        Connecting = QAbstractSocket.SocketState.ConnectingState
        Connected = QAbstractSocket.SocketState.ConnectedState
        Bound = QAbstractSocket.SocketState.BoundState
        Listening = QAbstractSocket.SocketState.ListeningState
        Closing = QAbstractSocket.SocketState.ClosingState

        def __new__(cls, value):
            return QAbstractSocket.SocketState(value)


class AbsSocket(AbsSocketMix, QAbstractSocket):
    ...


class WebSocket(QWebSocket):
    def __init__(self):
        super().__init__()
        self.stateChanged.connect(self.on_state_changed)
        self.textMessageReceived.connect(self.on_text_received)
        self.binaryMessageReceived.connect(self.on_binary_received)

    def on_state_changed(self, state: AbsSocket.SocketState) -> None:
        ...

    def on_text_received(self, text: str) -> None:
        ...

    def on_binary_received(self, data: QByteArray) -> None:
        ...
