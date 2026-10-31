# Notes for installing:
1. Clone the git repo into your rpi: (Use --recurse-submodules)
```bash
git clone --recurse-submodules https://github.com/eunalian/MICO
```

2. (Requires uv & pyinstaller) Compile `rpi-rgb-led-matrix` submodule then compile python script:
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