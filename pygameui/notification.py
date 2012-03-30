import pygame

import dialog
import window
import label
import theme
import asset


DOWN = 0
UP = 1
IDLE = 2


class NotificationView(dialog.DialogView):
    """A notification that drops down from the top of
    the window for a few seconds

    autoclose
        Automatically close the notification.

    autoclosetimeout
        How long to wait before closing the notification.
        Default: 3 (seconds).

    """

    def __init__(self, msg):
        message_label = label.Label(pygame.Rect((0, 0),
            (window.rect.w // 3, window.rect.h // 2)), msg,
            text_color=theme.dark_gray_color,
            font=asset.default_font, wrap_mode=label.WORDWRAP)

        message_label.shrink_wrap()
        text_size = message_label.text_size
        padding = min(20, window.rect.w // 8)
        framesize = (text_size[0] + padding * 2, text_size[1] + padding * 2)
        dialog.DialogView.__init__(self, pygame.Rect((0, 0), framesize))

        self.background_color = theme.main_gradient_colors
        self.border_color = theme.dark_accent_color
        self.border_width = 2

        self.autoclose = True
        self.autocloseafter = 3
        self.elapsed = 0

        message_label.frame.topleft = (padding, padding)
        message_label.background_color = self.background_color
        self.add_child(message_label)

    def appeared(self):
        self.frame.top = -self.frame.h
        self.frame.centerx = window.rect.w // 2
        self.state = DOWN

    def mouse_down(self, button, point):
        dialog.DialogView.mouse_down(self, button, point)
        self.state = UP

    def update(self, dt):
        dialog.DialogView.update(self, dt)
        if self.state == DOWN:
            if self.frame.top < -self.border_width:
                self.frame.top += dt * self.frame.h * 3
                self.frame.top = min(self.frame.top, -self.border_width)
            else:
                self.state = IDLE
        elif self.state == UP:
            if self.frame.top > -self.frame.h:
                self.frame.top -= dt * self.frame.h * 3
            else:
                self.rm()
        elif self.state == IDLE:
            self.elapsed += dt
            if self.elapsed > self.autocloseafter:
                self.state = UP