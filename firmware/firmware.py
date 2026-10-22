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
gifs_list = []
if len(sys.argv) < 2:
    sys.exit("Require a gif argument")
else:
    for i in range(sys.argv):
        gifs_list.append(sys.argv)


gif = Image.open(gifs_list[1])

try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("provided image is not a gif")


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Preprocess the gifs frames into canvases to improve playback performance
frames = []
canvas = matrix.CreateFrameCanvas()
print("Preprocessing gif, this may take a moment depending on the size of the gif...")
for frame_index in range(0, num_frames):
    gif.seek(frame_index)
    # must copy the frame out of the gif, since thumbnail() modifies the image in-place
    frame = gif.copy()
    frame.thumbnail((matrix.width, matrix.height), Image.LANCZOS)
    frames.append(frame.convert("RGB"))

# Close the gif file to save memory now that we have copied out all of the frames
gif.close()

print("Completed Preprocessing, displaying gif")

try:
    print("Press CTRL-C to stop.")

    # Infinitely loop through the gif
    cur_frame = 0
    while(True):
        canvas.SetImage(frames[cur_frame])
        matrix.SwapOnVSync(canvas, framerate_fraction=10)
        if cur_frame == num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
except KeyboardInterrupt:
    sys.exit(0)