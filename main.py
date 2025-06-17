import toml
import argparse
from pynput import keyboard
import sys
import playback
import record

# arguments
parser = argparse.ArgumentParser(description="llmacro - by EN")
parser.add_argument("file",type=str,help="Where to record/play macros")
parser.add_argument("--play",action="store_true",help="playback mode")
parser.add_argument("--loop",action="store_true",help="loop mode")
arguments = parser.parse_args()

# input settings
input_settings = toml.load("./shortcuts.toml")
start_macro = input_settings["start"]
stop_macro = input_settings["stop"]
print(f"press \"{start_macro}\" to start recording/playback")
print(f"press \"{stop_macro}\" to stop recording/playback")

# create settings
macro_settings = {
        "file":arguments.file,
        "play":arguments.play,
        "loop":arguments.loop,
        "start":keyboard.KeyCode.from_char(start_macro),
        "stop":keyboard.KeyCode.from_char(stop_macro)
        }

# begin playback/recording
with keyboard.Events() as events:
    for event in events:
        if event.key == macro_settings["start"]:
            break
if macro_settings["play"]:
    print("begin playing macro")
    playback.begin(macro_settings)
    print("done playing macro")
else:
    print("begin recording macro")
    record.begin(macro_settings)
    print("done recording macro")
