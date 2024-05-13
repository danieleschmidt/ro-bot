# /model/base/base.py

from PySide6 import QtCore

# for some reason PyCharm fails to resolve Signal in QtCore when importing
Signal = QtCore.Signal

class BaseObject(QtCore.QObject):

    def __init__(self):
        super(BaseObject, self).__init__()
