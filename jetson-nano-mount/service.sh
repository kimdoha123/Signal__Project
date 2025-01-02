#!/bin/bash
SERVICE_NAME="signal-masters.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
WORKDIR="/home/jsnano/repo/signal-masters/.devcontainer"
SCRIPT_NAME="run.py"
JSON_FILE=".devcontainer/devcontainer.json"
CONTAINER_NAME=$(grep '"--name",' "$JSON_FILE" | perl -pe 's/.*"--name",\s*"([^"]+)".*/\1/')
# 🔍 Explanation of Perl command options:
#   -p: Reads each input line, applies the Perl code, and prints the modified result automatically.
#   -e: Executes the given Perl code inline from the command line.

#   📝 Explanation of the regular expression:
#   s/.*"--name",\s*"([^"]+)".*/\1/
#   1. .*              -> Matches everything before "--name", including preceding text.
#   2. \s*             -> Matches zero or more whitespace characters.
#   3. "([^"]+)"       -> Captures the text inside the quotes as the first capture group.
#   4. \1              -> Returns the first capture group (the container name).


# 📝 Create, enable, and start the service
init_service() {
    echo "Creating $SERVICE_NAME..."

    # 🛠️ Write the systemd service file
  sudo bash -c "tee $SERVICE_PATH > /dev/null <<EOF
[Unit]
Description=Run Python script signal-masters-jetson-nano inside Docker container on startup
After=docker.service
Requires=docker.service

[Service]
User=jsnano
WorkingDirectory=$WORKDIR
ExecStartPre=/usr/bin/docker restart $CONTAINER_NAME
ExecStart=/usr/bin/docker exec -w /workspaces/signal-masters $CONTAINER_NAME python3 $SCRIPT_NAME
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

    echo "Reloading systemd and enabling $SERVICE_NAME..."
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    echo "$SERVICE_NAME created, enabled, and started successfully."
}

# 🔍 Check the status of the service
check_status() {
    sudo systemctl status "$SERVICE_NAME"
}

# 🚀 Enable the service (auto-start on boot)
enable_service() {
    echo "Enabling $SERVICE_NAME..."
    sudo systemctl enable "$SERVICE_NAME"
    echo "$SERVICE_NAME is now enabled."
}

# 🟢 Start the service immediately
start_service() {
    echo "Starting $SERVICE_NAME..."
    sudo systemctl start "$SERVICE_NAME"
    echo "$SERVICE_NAME started."
}

# ⛔ Disable the service (prevent auto-start on boot)
disable_service() {
    echo "Disabling $SERVICE_NAME..."
    sudo systemctl disable "$SERVICE_NAME"
    echo "$SERVICE_NAME is now disabled."
}

# 🛑 Stop the service
stop_service() {
    echo "Stopping $SERVICE_NAME..."
    sudo systemctl stop "$SERVICE_NAME"
    echo "$SERVICE_NAME stopped."
}

# 🗂️ Usage instructions as comments
: '
Usage:
  ./signal-masters.sh init      # Create, enable, and start the service
    >> Expect output:
      Reloading systemd and enabling signal-masters.service...
      Created symlink /etc/systemd/system/multi-user.target.wants/signal-masters.service → /etc/systemd/system/signal-masters.service.
      signal-masters.service created, enabled, and started successfully.
  ./signal-masters.sh status    # Check the status of the service
  ./signal-masters.sh enable    # Enable the service (auto-start on boot)
  ./signal-masters.sh disable   # Disable the service (prevent auto-start on boot)
  ./signal-masters.sh start     # Start the service immediately
  ./signal-masters.sh stop      # Stop the service
'

# 🧩 Process the command-line argument
case "$1" in
    init)
        init_service
        ;;
    status)
        check_status
        ;;
    enable)
        enable_service
        ;;
    start)
        start_service
        ;;
    disable)
        disable_service
        ;;
    stop)
        stop_service
        ;;
    *)
        echo "Usage: $0 {init|status|enable|start|disable|stop}"
        return 1
        ;;
esac
