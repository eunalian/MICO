# THIS FILE IS ADAPTED FROM HZELLER'S REPO (rpi-rgb-led-matrix/bindings/python/README.md)

#!/usr/bin/env python
import time
import sys
from PIL import Image
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

# completely forgot that id need to move the options block before the class
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
            frame.thumbnail((matrix.width, matrix.height), Image.LANCZOS)
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

gif_object_list = []
if len(sys.argv) < 2:
    sys.exit("Require a gif argument")
else:
    # now i need to make a new gif object for each gif in the sysargv
    for i in range(1, len(sys.argv)):
        append = gif(sys.argv[i], i-1)
        gif_object_list.append(append)

print(f"done processing gifs!!!! {str(gif_object_list)}")

canvas = matrix.CreateFrameCanvas()

# edit this to change later depending on keyboard presses!
current_gif = gif_object_list[1]

try:
    print("Press CTRL-C to stop.")

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

except KeyboardInterrupt:
    sys.exit(0)