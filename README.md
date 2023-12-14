# Overview 
This repo contains rudimentary code, capable of extracting multiple golf shots (video clips), from a video containing multiple golf shots. Indivisual golf shots are detected using peaks in the audio.

# Configuration

*Clip length*

A strike refers to the moment the golf club makes contact with the ball. PRE_STRIKE and POST_STRIKE are parameters that control how many seconds before and after the strike are captured. 

*Hit threshold*

To find each golf shot, the code searchs for audio peaks that are above the HIT_THRESHOLD parameter. This should a float between 0 (min noise) and 1 (max noise).

This will change with factors such as club choice, distance of camera from the ball, and the level of background noise.
