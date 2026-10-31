# THIS FILE IS ADAPTED FROM HZELLER'S REPO (rpi-rgb-led-matrix/bindings/python/README.md)

#!/usr/bin/env python
import time
import os
import sys
from PIL import Image

# dude i think i have to use evdev instead
# im stupid . i tried compiling the rgbmatrix library on my mac, this is the better method apparently

if sys.platform == "darwin":
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
    from pynput import keyboard
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    import evdev
    import threading
    # it says event1 in my rpi's evtest but im not sure if its gonna be the same everywhere else!!!!!!!!! omg
    device = evdev.InputDevice("/dev/input/by-id/usb-8BitDo_8BitDo_Retro_Keyboard_Receiver-if02-event-kbd")
    

# 21.10.26: maybe i should make a class for every gif so that it may contain its own frames and stuff
# bro i dont get it im so fucking sleepy :sob:
# on second thought, maybe this is a bad idea, why make a class if the gif is already part of some other class

# 22.10.26: i am so sleepy but i think i need to like rubber ducky this thing
# i need to iteratively load each gif listed in the system arguments into a class for gifs and then load each of their frames into matrix canvas thingymabob

# 23.10.26: well how is the gif even processed in the original hzeller demo file?
# 1: gif variable created, calls Image.open() on the first argument in sys.argv
# 2: num_frames variable created, calls gif.n_frames to get the number of frames
# 3: for loop that iterates through gif frames then .thumbnail() to make it smaller then yada yada yada append to frames array
# the next problem to solve is how to switch between different gifs in the matrix canvas

# i think i need to include a method that closes a gif, ran after processing is done?

# completely forgot that id need to move the optionps block before the class
# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.show_refresh_rate = True
options.pixel_mapper_config = "Rotate:180"
options.drop_privaleges = False

matrix = RGBMatrix(options = options)

class gif:
    def __init__(self, location, gif_index):
        self.location = location

        # dude i lowk dont know if we even need the gif_index lmao
        self.gif_index = gif_index
        self.frames = self.process_frames()
        self.fps = self.detect_fps()

    # input a gif, return back an array of frames in self.frames
    def process_frames(self):
        frames = []
        pregif = Image.open(self.location)

        try:
            self.num_frames = pregif.n_frames
        except Exception:
            sys.exit(f"{self.location} is not a gif")
        
        print(f"Preprocessing gif {self.location}, index {self.gif_index}.")
        for frame_index in range(0, self.num_frames):
            pregif.seek(frame_index)
            # must copy the frame out of the gif, since thumbnail() modifies the image in-place
            frame = pregif.copy()
            frame.thumbnail((matrix.width, matrix.height), Image.NEAREST)
            frames.append(frame.convert("RGB"))

        # close the gif after processing is done to save memory
        pregif.close()
        return frames

    def detect_fps(self):
        # adapted from stackOverFlow lol
        # Returns the average framerate of a PIL Image object
        pregif = Image.open(self.location)
        pregif.seek(0)
        frames = duration = 0
        while True:
            try:
                frames += 1
                duration += pregif.info['duration']
                pregif.seek(pregif.tell() + 1)
            except EOFError:
                return frames / duration * 1000
        return None

        
# MAIN:

default_gif_list = []

# this is prob better than hard coding everything
for i in sorted(os.listdir("../face-art")):
    default_gif_list.append(os.path.join("../face-art", i))

gif_object_list = []
cur_frame = 0

# decide to use default gif list, or to use system arguments
if len(sys.argv) < 2:
    print("using default gif list:")
    for i in range(len(default_gif_list)):
        append = gif(default_gif_list[i], i-1)
        gif_object_list.append(append)
else:
    # now i need to make a new gif object for each gif in the sysargv
    for i in range(len(sys.argv)):
        append = gif(sys.argv[1:], i-1)
        gif_object_list.append(append)

print(f"done processing gifs!!!! {str(gif_object_list)}")

canvas = matrix.CreateFrameCanvas()

# edit this to change later depending on keyboard presses!
current_gif = gif_object_list[0]

# handle switching keys using keyboard F row
# on some BULLSHIT right now because last minute i have to change to evdev cause i realized pynput doesnt work on headless env
if sys.platform == "darwin":
    def on_press(key):

        # what the fuck is a global variable
        global current_gif, cur_frame

        #lowk got this from ai cause i dont know how this library works
        # i had no idea what isinstance() is before now
        if isinstance(key, keyboard.Key) and key.name.startswith("f") and key.name[1:].isdigit():
            f_number = int(key.name[1:])

            try:
                print(f"switched to gif index {f_number - 1}")
                current_gif = gif_object_list[(f_number - 1)]
                # set the current frame to 0
                
            except IndexError:
                print(f"gif {f_number - 1} out of range")
else:
    F_KEY_TO_GIF_INDEX = {
    evdev.ecodes.KEY_F1: 0,
    evdev.ecodes.KEY_F2: 1,
    evdev.ecodes.KEY_F3: 2,
    evdev.ecodes.KEY_F4: 3,
    evdev.ecodes.KEY_F5: 4,
    evdev.ecodes.KEY_F6: 5,
    evdev.ecodes.KEY_F7: 6,
    evdev.ecodes.KEY_F8: 7,
    evdev.ecodes.KEY_F9: 8,
    evdev.ecodes.KEY_F10: 9,
    evdev.ecodes.KEY_F11: 10,
    evdev.ecodes.KEY_F12: 11,
    }

    def keyboard_loop():
        global current_gif, cur_frame
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                gif_index = F_KEY_TO_GIF_INDEX.get(event.code)
                try:
                    print(f"switched to gif index {gif_index}")
                    current_gif = gif_object_list[(gif_index)]
                    # set the current frame to 0
                    cur_frame = 0
                except IndexError:
                    print(f"gif {gif_index} out of range")




try:
    print("Press CTRL-C to stop.")

    # handle catching keyboard listener events
    if sys.platform == "darwin":
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    else:
        thread = threading.Thread(target=keyboard_loop, daemon=True)
        thread.start()



    # Infinitely loop through the gif
    # oh lol its as easy as using the object attributes of the same name

    while(True):
        canvas.SetImage(current_gif.frames[cur_frame])

        # i dont know how to set the frame rate lmao
        matrix.SwapOnVSync(canvas, framerate_fraction=1)
        if cur_frame == current_gif.num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
        time.sleep(1.0/current_gif.fps)

except KeyboardInterrupt:
    sys.exit(0)