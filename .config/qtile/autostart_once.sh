#!/bin/bash
nitrogen --restore &&
wal -b 282738 -i ~/Wallpaper/Aesthetic2.png &&
picom --backend glx --xrender-sync-fence &&
greenclip daemon &
