# robot.py

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMainWindow, QStyle

import logging

from data.process import KeyboardHook
from model.base import Rectangle
from model.game import Game
from model.actor import Actor
from view import MapView

log = logging.getLogger('app.robot')

class Robot(QMainWindow):

    def __init__(self, app, window_name, process_name):
        super(Robot, self).__init__()
        log.debug('Initializing Robot')
        self.app = app
        self.active = False

        screens = self.app.screens()
        self.scr_1 = screens[0].availableGeometry()
        log.debug(f'Screen 1 geometry: {self.scr_1}')
        if len(screens) > 1:
            self.scr_2 = screens[1].availableGeometry()
        else:
            self.scr_2 = self.scr_1  # Use the same geometry as scr_1 if there's only one screen
        log.debug(f'Screen 2 geometry: {self.scr_2}')

        self._init_keyboard_hook()
        self._init_map_view()
        self._init_game(window_name, process_name)
        self._init_actor()

        # initialise game state before starting workers
        self.read_game_state()

        self._init_timers()

        self.show()

    def _init_keyboard_hook(self):
        log.debug('Initializing keyboard hook')
        self.keyboard_hook = KeyboardHook()
        self.keyboard_hook.set_callback(self.toggle_activity, (19,))  # pause button

    def _init_map_view(self):
        log.debug('Initializing map view')
        self.map_view = MapView(self)
        self.setCentralWidget(self.map_view)

    def _init_game(self, window_name, process_name):
        log.debug(f'Initializing game with window_name: {window_name}, process_name: {process_name}')
        self.game = Game(window_name, process_name)
        self.game.window.center(Rectangle(self.scr_1))
        self.game.updated.map.connect(self.slot_map)

    def _init_actor(self):
        log.debug('Initializing actor')
        self.actor = Actor(self.game, Rectangle(self.scr_1))
        self.actor.route.updated.path.connect(self.map_view.slot_path)
        self.actor.route.updated.zones.connect(self.map_view.slot_zones)

    def _init_timers(self):
        log.debug('Initializing timers')
        self.timer_keyboard = QTimer()
        self.timer_keyboard.timeout.connect(self.keyboard_hook.flush)
        self.timer_keyboard.start(100)

        self.timer_game = QTimer()
        self.timer_game.timeout.connect(self.read_game_state)
        self.timer_game.start(100)

        self.timer_actor = QTimer()
        self.timer_actor.timeout.connect(self.act)
        self.timer_actor.start(500)

    def closeEvent(self, event):
        log.debug('Closing Robot')
        self.keyboard_hook.close()
        super(Robot, self).closeEvent(event)

    def resizeEvent(self, event):
        log.debug('Resizing Robot')
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.map_view.size(),
                self.scr_2,
            )
        )

    def slot_map(self, map):
        log.debug('Slot map called')
        self.map_view.slot_map(map)
        self.adjustSize()

    def toggle_activity(self):
        if self.active:
            log.debug('Bot activity has been paused')
        else:
            log.debug('Bot activity has been resumed')
        self.active = not self.active

    def read_game_state(self):
        log.debug('Reading game state')
        self.game.read()
        self.map_view.update()

    def act(self):
        if self.active:
            log.debug('Acting')
            self.actor.act()
