# THIS FILE IS ADAPTED FROM HZELLER'S REPO (rpi-rgb-led-matrix/bindings/python/README.md)

#!/usr/bin/env python
import time
import sys

# im stupid . i tried compiling the rgbmatrix library on my mac, this is the better method apparently
if sys.platform == "darwin":
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.cols = 64
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()
# Make image fit our screen.
# orginally LANCZOS, changed to NEAREST cuz yk, pixels n stuff
image.thumbnail((matrix.width, matrix.height), Image.NEAREST)
matrix.SetImage(image.convert('RGB'))
canvas.SetImage(image.convert('RGB'))
canvas = matrix.SwapOnVSync(canvas)

# omg it works

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)