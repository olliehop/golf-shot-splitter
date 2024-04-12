# Overview 
This repo contains rudimentary code, capable of extracting each golf shot from a video containing multiple golf shots. Individual golf shots are detected using audio peaks caused by the club stiking the ball.

# Purpose

When filming a golf swing for analysis, it is much more convenient to capture the whole session or a series of shots. This results in a long video file that is difficult to navigate, compare swings and often has large gaps between swings. Having each swing saved individually, with a fixed length of time before and after impact, allows for much easier comparison and categorisation of swings that show certain issues.

# Configuration

*Environment file*

VIDEO_PATH - Full path to original video

OUT_DIR - Directory for exporting clips to

*Clip length*

A strike refers to the moment the golf club makes contact with the ball. PRE_STRIKE and POST_STRIKE are parameters that control how many seconds before and after the strike are captured. 

*Hit threshold*

To find each golf shot, the code searchs for audio peaks that are above the HIT_THRESHOLD parameter. This should a float between 0 (min noise) and 1 (max noise).

This will change with factors such as club choice, distance of camera from the ball, and the level of background noise.