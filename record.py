from pynput import *
import pickle
import time
settings = None
last_time = 0
inputs = []

# callbacks for recording the keys
def callback_move_mouse(x,y,injected):
    global last_time
    global settings
    global inputs
    current_time = time.time()-last_time
    last_time = time.time()
    inputs.append([current_time,"move",x,y])
def callback_button_mouse(x,y,button,pressed,injected):
    global last_time
    global settings
    global inputs
    current_time = time.time()-last_time
    last_time = time.time()
    inputs.append([current_time,"button",x,y,button,pressed])
def callback_scroll_mouse(x,y,dx,dy,injected):
    global last_time
    global settings
    global inputs
    current_time = time.time()-last_time
    last_time = time.time()
    inputs.append([current_time,"scroll",x,y,dx,dy])
def callback_press_key(key,injected):
    global last_time
    global settings
    global inputs
    if key != settings["start"] and key != settings["stop"]:
        current_time = time.time()-last_time
        last_time = time.time()
        inputs.append([current_time,"key_down",key])
        return
def callback_release_key(key,injected):
    global last_time
    global settings
    global inputs
    if key != settings["start"] and key != settings["stop"]:
        current_time = time.time()-last_time
        last_time = time.time()
        inputs.append([current_time,"key_up",key])
        return

# start recording
def begin(macro_settings):
    # load settings
    global last_time
    global settings
    global inputs
    last_time = time.time()
    settings = macro_settings
    mouse_controller = mouse.Controller()
    inputs = [[0,"move",mouse_controller.position[0],mouse_controller.position[1]]]

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
                write_inputs = open(settings["file"],"wb")
                pickle.dump(inputs,write_inputs)
                write_inputs.close()
                return
