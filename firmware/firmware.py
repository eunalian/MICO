# /// script
# dependencies = [
#     "appnope==1.0.0",
#     "asttokens==3.0.2",
#     "attrs==26.1.0",
#     "backcall==0.2.0",
#     "beautifulsoup4==4.15.0",
#     "bleach==6.4.0",
#     "certifi==2026.10.23",
#     "charset-normalizer==3.5.2",
#     "decorator==5.3.1",
#     "defusedxml==0.7.1",
#     "docopt==0.6.2",
#     "executing==2.3.0",
#     "fastjsonschema==2.22.2",
#     "idna==3.20",
#     "ipython==8.12.3",
#     "jedi==0.20.1",
#     "jinja2==3.1.6",
#     "jsonschema==4.26.0",
#     "jsonschema-specifications==2025.9.1",
#     "jupyter-client==8.10.0",
#     "jupyter-core==5.9.1",
#     "jupyterlab-pygments==0.3.0",
#     "markupsafe==3.0.4",
#     "matplotlib-inline==0.2.2",
#     "mistune==3.4.0",
#     "nbclient==0.11.0",
#     "nbconvert==7.17.2",
#     "nbformat==5.11.1",
#     "packaging==26.3",
#     "pandocfilters==1.5.1",
#     "parso==0.8.7",
#     "pexpect==4.9.0",
#     "pickleshare==0.7.5",
#     "pillow==13.0.0",
#     "pipreqs==0.5.0",
#     "platformdirs==4.13.6",
#     "prompt-toolkit==3.0.53",
#     "ptyprocess==0.7.0",
#     "pure-eval==0.2.4",
#     "pygments==2.21.0",
#     "pynput==1.8.2",
#     "pyobjc-core==12.2.2",
#     "pyobjc-framework-applicationservices==12.2.2",
#     "pyobjc-framework-cocoa==12.2.2",
#     "pyobjc-framework-coretext==12.2.2",
#     "pyobjc-framework-quartz==12.2.2",
#     "python-dateutil==3.0.0",
#     "pyzmq==27.2.0",
#     "referencing==0.37.0",
#     "requests==2.34.2",
#     "rgbmatrixemulator>=0.20.0",
#     "rpds-py==2026.9.1",
#     "six==1.17.0",
#     "soupsieve==3.0.4",
#     "stack-data==0.6.3",
#     "tinycss2==1.5.1",
#     "tornado==6.6",
#     "traitlets==5.16.1",
#     "typing-extensions==4.16.0",
#     "tzdata==2026.5",
#     "urllib3==2.8.0",
#     "wcwidth==0.9.4",
#     "webencodings==0.6.1",
#     "yarg==0.1.9",
# ]
# ///

# THIS FILE IS ADAPTED FROM HZELLER'S REPO (rpi-rgb-led-matrix/bindings/python/README.md)

#!/usr/bin/env python
import time
import sys
from PIL import Image
from pynput import keyboard
# im stupid . i tried compiling the rgbmatrix library on my mac, this is the better method apparently

if sys.platform == "darwin":
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

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

# dude i dont know why but the code always selects starting from index one so like ill just put nothing on the first index
default_gif_list = ['face-art/neutral.gif', 'face-art/smile-blush.gif', 'face-art/blush.gif', 'face-art/angry.gif', 'face-art/closedsmile.gif', 'face-art/flowery.gif',]
gif_object_list = []

if len(sys.argv) < 2:
    print("using default gif list:")
    for i in range(len(default_gif_list)):
        append = gif(default_gif_list[i], i-1)
        gif_object_list.append(append)
else:
    # now i need to make a new gif object for each gif in the sysargv
    for i in range(len(sys.argv)):
        append = gif(sys.argv[i], i-1)
        gif_object_list.append(append)

print(f"done processing gifs!!!! {str(gif_object_list)}")

canvas = matrix.CreateFrameCanvas()

# edit this to change later depending on keyboard presses!
current_gif = gif_object_list[0]

# handle switching keys using keyboard F row
def on_press(key):

    # what the fuck is a global variable
    global current_gif

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

try:
    print("Press CTRL-C to stop.")

    # handle catching keyboard listener events
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Infinitely loop through the gif
    # oh lol its as easy as using the object attributes of the same name

    cur_frame = 0
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