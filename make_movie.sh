#!/bin/bash

ffmpeg -framerate 60 -i frames/frame-%03d.png -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" starmap.mp4 -y

rm frames/frame-*.png
