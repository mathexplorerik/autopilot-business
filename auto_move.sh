#!/bin/bash
echo "👀 Watching Downloads folder..."
while true; do
    for file in ~/Downloads/DALL*.png ~/Downloads/ChatGPT*.png; do
        if [ -f "$file" ]; then
            mv "$file" ~/Desktop/autopilot-business/downloads/
            echo "✅ Moved: $(basename $file)"
        fi
    done
    sleep 3
done
