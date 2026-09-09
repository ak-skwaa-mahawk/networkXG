#!/data/data/com.termux/files/usr/bin/bash
TARGET="/data/data/com.termux/files/home/networkXG/daemon.log"
MAX_SIZE=512000 # 500 KB

if [ -f "$TARGET" ]; then
    SIZE=$(wc -c < "$TARGET")
    if [ "$SIZE" -gt "$MAX_SIZE" ]; then
        tail -n 1000 "$TARGET" > "$TARGET.tmp" && mv "$TARGET.tmp" "$TARGET"
        echo "[$(date -u)] daemon.log rotated to 1000 lines." >> /data/data/com.termux/files/home/networkXG/ens_legis.log
    fi
fi
