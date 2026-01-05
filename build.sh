#!/bin/sh
python rss.py index
emacs -Q --script build-site.el
python rss.py feed
python postprocess.py 
