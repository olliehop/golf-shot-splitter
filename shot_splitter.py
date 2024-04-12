import os
import numpy as np

from pathlib import Path
import moviepy.editor as mpy
from scipy.signal import find_peaks
from dotenv import load_dotenv


load_dotenv() 

PRE_STRIKE = 3 # Capture seconds before strike
POST_STRIKE = 2 # Capture seconds after strike
HIT_THRESHOLD = 0.90 # Find sound peaks over (0 < threshold < 1)

VIDEO_PATH = Path(os.getenv('VIDEO_PATH')) # Full path to original video
OUT_DIR = Path(os.getenv('OUT_DIR')) # Directory for exporting clips to

def get_max_frame_audio(raw_clip) -> tuple:
    """Returns max audio value for each frame.
    
    Audio has much higher resolution than video. Group audio data points to align with video frames
    then find the max within each group.
    """
    frame_duration = 1/raw_clip.fps
    
    # Iterate over audio using the duration (s) of each frame
    frame_chunks = raw_clip.audio.iter_chunks(chunk_duration=frame_duration)
    return tuple(np.max(chunk) for chunk in frame_chunks)

def find_strikes(max_frame_audio,  fps) -> tuple:
    """Return time (s) of each strike"""
    min_gap = 5*fps # Min time between peaks
    hit_frames, _ = find_peaks(max_frame_audio, height=HIT_THRESHOLD, distance=min_gap)
    return tuple(hf/fps for hf in hit_frames) # Convert from frame number to time

def get_shot_times(strikes) -> tuple:
    """Returns a nested tuple containing the start, end time of each shot"""
    return tuple((s-PRE_STRIKE, s+POST_STRIKE) for s in strikes)

def export_shots(raw_clip, shot_times, base_name) -> None:
    """Exports clips to desired directory"""

    print(f'Exporting {len(shot_times)} shots...')
    
    for i, (start, end) in enumerate(shot_times, start=1):
        filepath = OUT_DIR / f'{base_name}_{i}.mp4'
        shot = raw_clip.subclip(start, end)
        shot.write_videofile(filepath)
    return None

if __name__ == '__main__':
    
    video = mpy.VideoFileClip(VIDEO_PATH, target_resolution=(1920, 1080))

    frame_audio = get_max_frame_audio(video)
    strikes = find_strikes(frame_audio, video.fps)
    shot_times = get_shot_times(strikes)

    export_shots(video, shot_times, VIDEO_PATH.stem)