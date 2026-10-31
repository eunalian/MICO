sudo apt install kbd
sudo modprobe uinput

echo "Adding systemd unit:"
sudo tee /etc/systemd/system/mico.service << EOF
[Unit]
Description=MICO, Hub75 TV Head control
Documentation=https://github.com/eunalian/MICO

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/firmware/dist/firmware
Restart=always
Environment=PYNPUT_BACKEND_KEYBOARD=uinput

[Install]
WantedBy=multi-user.target
EOF
