from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSTimer
import objc
import os


class PomodoroTimer(object):

    def __init__(self):
        self.duration = 1500  # default duration of 25 minutes in seconds
        self.break_duration = 300  # default break duration of 5 minutes in seconds
        self.remaining_time = self.duration
        self.break_remaining_time = self.break_duration
        self.timer = None
        self.break_timer = None
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.statusitem.setTitle_('Studying: {:02d}:{:02d}'.format(25, 0))
        self.statusitem.setHighlightMode_(True)
        self.statusitem.setToolTip_('Pomodoro Timer')

        # create menu for the statusitem
        self.menu = NSMenu.alloc().init()
        self.start_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Start", "startTimer:", "")
        self.start_menu_item.setTarget_(self)
        self.menu.addItem_(self.start_menu_item)
        self.stop_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Stop", "stopTimer:", "")
        self.stop_menu_item.setTarget_(self)
        self.menu.addItem_(self.stop_menu_item)
        self.reset_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Reset", "resetTimer:", "")
        self.reset_menu_item.setTarget_(self)
        self.menu.addItem_(self.reset_menu_item)
        self.menu.addItem_(NSMenuItem.separatorItem())
        self.duration_menu = NSMenu.alloc().initWithTitle_("Duration")
        self.duration_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Duration", None, "")
        self.duration_menu_item.setSubmenu_(self.duration_menu)
        self.menu.addItem_(self.duration_menu_item)
        self.duration_menu_items = []
        for duration in [10, 60 * 25, 60 * 30, 60 * 35, 60 * 40, 60 * 45, 60 * 50, 60 * 55, 60 * 60]:  # study durations
            menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("{} minutes".format(duration // 60),
                                                                               "setDuration:", "")
            menu_item.setRepresentedObject_(duration)
            menu_item.setTarget_(self)
            self.duration_menu_items.append(menu_item)
            self.duration_menu.addItem_(menu_item)
        self.break_duration_menu = NSMenu.alloc().initWithTitle_("Break Duration")
        self.break_duration_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Break Duration",
                                                                                               None, "")
        self.break_duration_menu_item.setSubmenu_(self.break_duration_menu)
        self.menu.addItem_(self.break_duration_menu_item)
        self.break_duration_menu_items = []
        for break_duration in [10, 60 * 5, 60 * 6, 60 * 7, 60 * 8, 60 * 9, 60 * 10]:  # break durations
            menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "{} minutes".format(break_duration // 60),
                "setBreakDuration:", "")
            menu_item.setRepresentedObject_(break_duration)
            menu_item.setTarget_(self)
            self.break_duration_menu_items.append(menu_item)
            self.break_duration_menu.addItem_(menu_item)
        self.statusitem.setMenu_(self.menu)

    def send_notification(self, message):
        title = "Pomodoro Timer"
        os.system("""
                      osascript -e 'display notification "{}" with title "{}"'
                      """.format(message, title))

    def startTimer_(self, sender):
        if self.break_timer and self.break_remaining_time > 0:
            self.startBreak_(None)
        else:
            # invalidate any previous timer
            if self.timer:
                self.timer.invalidate()
            # set the remaining time only if the timer is not running
            if self.remaining_time <= 0:
                self.remaining_time = self.duration
            # update the status item
            self.update_status_item()
            # start the timer
            self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(1.0, self,
                                                                                                  'update_time', None,
                                                                                                  True)

    def startBreak_(self, sender):
        # invalidate any previous timer
        if self.break_timer:
            self.break_timer.invalidate()
        # set the remaining time only if the timer is not running
        if self.break_remaining_time <= 0:
            self.break_remaining_time = self.break_duration
        # update the status item
        self.update_status_item()
        # start the timer
        self.break_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(1.0, self,
                                                                                                    'update_break_time',
                                                                                                    None, True)

    def stopTimer_(self, sender):
        if self.timer:
            self.timer.invalidate()
        if self.break_timer:
            self.break_timer.invalidate()
        self.update_status_item()

    def resetTimer_(self, sender):
        # invalidate the timer
        if self.timer:
            self.timer.invalidate()
        # reset the remaining time
        self.remaining_time = self.duration
        # update the status item
        self.update_status_item()

    def resetBreak_(self, sender):
        # invalidate the timer
        if self.break_timer:
            self.break_timer.invalidate()
        # reset the remaining time
        self.break_remaining_time = self.break_duration
        # update the status item
        self.update_break_status_item()

    def setDuration_(self, sender):
        self.duration = sender.representedObject()
        self.resetTimer_(None)

    def setBreakDuration_(self, sender):
        self.break_duration = sender.representedObject()
        self.resetBreak_(None)

    def update_time(self):
        print(self.remaining_time)
        self.remaining_time -= 1
        self.update_status_item()
        if self.remaining_time <= 0:
            self.timer.invalidate()
            # start the timer after the break is finished
            self.startBreak_(None)
            # add a notification for when the study is done
            self.send_notification("Study is Done, take a break")

    def update_break_time(self):
        self.break_remaining_time -= 1
        self.update_status_item()
        if self.break_remaining_time <= 0:
            self.break_timer.invalidate()
            # start the timer after the break is finished
            self.startTimer_(None)
            # add a notification for when the study is done
            self.send_notification("Break is Done, start studying again")

    def update_status_item(self):
        # indicate if you're studying or not
        if self.remaining_time > 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.statusitem.setTitle_('Studying: {:02d}:{:02d}'.format(minutes, seconds))
        else:
            minutes = self.break_remaining_time // 60
            seconds = self.break_remaining_time % 60
            self.statusitem.setTitle_('Break: {:02d}:{:02d}'.format(minutes, seconds))

if __name__ == '__main__':
    app = NSApplication.sharedApplication()
    pomodoro_timer = PomodoroTimer()
    app.setDelegate_(pomodoro_timer)
    app.run()
