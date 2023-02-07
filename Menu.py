from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSTimer
import subprocess
import objc
import os

# Import code from PomodoroTimer.py
from PomodoroTimer import PomodoroTimer

# Import code from MusicPlayer.py
from MusicPlayer import open_spotify

# Import code from DarkLightModeSwitch.py
from DarkLightModeSwitch import change_mode, get_current_mode

class MacOSMenuBar(object):

    def __init__(self):
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.statusitem.setTitle_('Placeholder Icon')
        self.statusitem.setHighlightMode_(True)
        self.statusitem.setToolTip_('MacOS Menu Bar')

        # create menu for the statusitem
        self.menu = NSMenu.alloc().init()
        self.pomodoro_timer_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Pomodoro Timer", "startPomodoroTimer:", "")
        self.pomodoro_timer_menu_item.setTarget_(self)
        self.menu.addItem_(self.pomodoro_timer_menu_item)
        self.music_player_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Music Player", "startMusicPlayer:", "")
        self.music_player_menu_item.setTarget_(self)
        self.menu.addItem_(self.music_player_menu_item)
        self.dark_light_mode_switch_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Dark/Light Mode Switch", "startDarkLightModeSwitch:", "")
        self.dark_light_mode_switch_menu_item.setTarget_(self)
        self.menu.addItem_(self.dark_light_mode_switch_menu_item)
        self.statusitem.setMenu_(self.menu)

    def startPomodoroTimer_(self, sender):
        pomodoro_timer = PomodoroTimer()
        app = NSApplication.sharedApplication()
        app.setDelegate_(pomodoro_timer)
        app.run()

    def startMusicPlayer_(self, sender):
        open_spotify()

    def startDarkLightModeSwitch_(self, sender):
        current_mode = get_current_mode()
        if current_mode == "true":
            change_mode("light")
        elif current_mode == "false":
            change_mode("dark")
        else:
            print("Could not determine current mode")
if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    macos_menu_bar = MacOSMenuBar()
    app.setDelegate_(macos_menu_bar)
    app.run()
