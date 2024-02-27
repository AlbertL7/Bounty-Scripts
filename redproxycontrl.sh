#!/bin/bash

ACTION=$1

if [ "$ACTION" = "start" ]; then
    echo "Activating proxy..."
    # Start redsocks service
    sudo systemctl start redsocks
    # Enable redsocks service to start on boot
    sudo systemctl enable redsocks
    # Check if the REDSOCKS chain already exists
    if sudo iptables -t nat -L REDSOCKS >/dev/null 2>&1; then
        echo "REDSOCKS chain already exists, flushing existing rules..."
        # Flush the existing REDSOCKS chain to remove all rules
        sudo iptables -t nat -F REDSOCKS
    else
        echo "Creating REDSOCKS chain..."
        sudo iptables -t nat -N REDSOCKS
    fi
    sudo iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345
    sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDSOCKS
    sudo iptables -t nat -A OUTPUT -p tcp --dport 443 -j REDSOCKS
elif [ "$ACTION" = "stop" ]; then
    echo "Deactivating proxy..."
    # Stop redsocks service
    sudo systemctl stop redsocks
    # Disable redsocks service from starting on boot
    sudo systemctl disable redsocks
    sudo iptables -t nat -D OUTPUT -p tcp --dport 80 -j REDSOCKS
    sudo iptables -t nat -D OUTPUT -p tcp --dport 443 -j REDSOCKS
    sudo iptables -t nat -F REDSOCKS
    sudo iptables -t nat -X REDSOCKS
else
    echo "Usage: $0 <start|stop>"
fi
