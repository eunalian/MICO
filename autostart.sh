REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
FIRMWARE_DIR="$REPO_DIR/firmware"

echo "Adding systemd unit:"
sudo tee /etc/systemd/system/mico.service << EOF
[Unit]
Description=MICO, Hub75 TV Head control
Documentation=https://github.com/eunalian/MICO

[Service]
Type=simple
WorkingDirectory=$FIRMWARE_DIR
ExecStart=$FIRMWARE_DIR/.venv/bin/python3 $FIRMWARE_DIR/firmware.py
Restart=on-failure
RestartSec=5
TimeoutStartSec=90

[Install]
WantedBy=multi-user.target
EOF
