echo "Adding systemd unit:"
sudo tee /etc/systemd/system/mico.service << EOF
[Unit]
Description=MICO, Hub75 TV Head control
Documentation=https://github.com/eunalian/MICO

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$HOME/.local/bin/uv run --no-sync firmware.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
