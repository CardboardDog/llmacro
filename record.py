from pynput import *
import time
settings = None
last_time = 0
inputs = []
def callback_move_mouse(x,y,injected):
    global last_time
    global settings
    global inputs
def callback_button_mouse(x,y,button,pressed,injected):
    global last_time
    global settings
    global inputs
def callback_scroll_mouse(x,y,dx,dy,injected):
    global last_time
    global settings
    global inputs
def callback_press_key(key,injected):
    global last_time
    global settings
    global inputs
    if key == settings["start"] or key == settings["stop"]:
        return
def callback_release_key(key,injected):
    global last_time
    global settings
    global inputs
    if key == settings["start"] or key == settings["stop"]:
        return
def begin(macro_settings):
    # load settings
    global last_time
    global settings
    global inputs
    last_time = time.time_ns()
    settings = macro_settings
    inputs = [
            ["move",mouse.position[0],mouse.position[1]]
            ]

    # setup callbacks
    mouse_listener = mouse.Listener(
            on_move=callback_move_mouse,
            on_click=callback_button_mouse,
            on_scroll=callback_scroll_mouse
            )
    keyboard_listener = keyboard.Listener(
            on_press = callback_press_key,
            on_release = callback_release_key
            )
    mouse_listener.start()
    keyboard_listener.start()

    # stop recording
    with keyboard.Events() as events:
        for event in events:
            if event.key == settings["stop"]:
                mouse_listener.stop()
                keyboard_listener.stop()
                return
