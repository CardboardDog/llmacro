from pynput import *
from threading import Event
import signal
import pickle
inputs = []
settings = None
mouse_controller = None
keyboard_controller = None
sleep_event = None
stopped = False

# callback used to detect stop key
def callback_press_key(key,injected):
    global stopped
    global settings
    if injected:
        return
    if key == settings["stop"]:
        stopped = True
        sleep_event.set()

# takes an input and performs the action
def handle_input(input_event):
    global mouse_controller
    global keyboard_controller
    if input_event[1] == "key_down":
        keyboard_controller.press(input_event[2])
    elif input_event[1] == "key_up":
        keyboard_controller.release(input_event[2])
    elif input_event[1] == "move":
        mouse_controller.position = (input_event[2],input_event[3])
    elif input_event[1] == "button":
        mouse_controller.position = (input_event[2],input_event[3])
        if input_event[5]:
            mouse_controller.press(input_event[4])
        else:
            mouse_controller.release(input_event[4])
    elif input_event[1] == "scroll":
        mouse_controller.position = (input_event[2],input_event[3])
        mouse_controller.scroll(input_event[4],input_event[5])

# start playback
def begin(macro_settings):
    # load settings
    global inputs
    global settings
    global mouse_controller
    global keyboard_controller
    global sleep_event
    global stopped
    settings = macro_settings
    read_inputs = open(settings["file"],"rb")
    inputs = pickle.load(read_inputs)
    read_inputs.close()
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()
    sleep_event = Event()
    stopped = False

    # setup callbacks
    keyboard_listener = keyboard.Listener(on_press = callback_press_key)
    keyboard_listener.start()

    # begin playing
    while not stopped:
        for input_event in inputs:
            sleep_event.wait(input_event[0]/1000000000) # convert nanoseconds to seconds
            if stopped:
               return 
            handle_input(input_event)
        if not settings["loop"]:
            return 

