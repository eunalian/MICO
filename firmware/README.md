# Notes for installing:
1. Clone the git repo into your rpi: (Use --recurse-submodules)
```bash
git clone --recurse-submodules https://github.com/eunalian/MICO
```

2. (Requires uv & pyinstaller) Compile `rpi-rgb-led-matrix` submodule then install the python modules with uv sync:
```bash
cd MICO/firmware
uv sync
```
3. Create a systemd unit to start the script automatically:
```bash
chmod +x ../autostart.sh
sudo ../autostart.sh
sudo systemctl enable --now mico.service
```

its lowk better to run this on like dietpi or something but i dont really know 

**Please change the evdev device listed in [firmware.py](firmware.py) (line 20) to your own input device!**

Find your input device with the following:
```bash
ls -l /dev/input/by-id/
