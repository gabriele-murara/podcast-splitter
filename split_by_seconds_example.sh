#! /bin/sh

# Splits '2_hours_of_podcast.mp3' into tracks of 10 minutes and prints
# logs to console
python main.py -f ~/Music/2_hours_of_podcast.mp3 -s 600 -o ~/Music/splitted_podcasts/ --verbose
