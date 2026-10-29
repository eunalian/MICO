echo "Installing uv:"
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Building rpi-rgb-led-matrix library:"
uv add rpi-rgb-led-matrix

# dude im too sleepy to think about how this works right now

cat << "EOF" > mico.service
