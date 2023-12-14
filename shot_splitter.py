import numpy as np
from pathlib import Path
from scipy.signal import find_peaks
import moviepy.editor as mpy


PRE_STRIKE = 3 # capture seconds before strike
POST_STRIKE = 2 # # capture seconds after strike
HIT_THRESHOLD = 0.90 # find sound peaks over (0 < threshold < 1)
CLIP_DIR = '/Users/oliver/Movies/Golf Analysis/Raw'
CLIP_NAME = 'VID_20230317_181856.mp4'
DEFAULT_OUT = Path('/Users/oliver/Movies/Golf Analysis/clips')

def get_max_frame_audio(raw_clip) -> tuple:
    """Returns max audio output for each frame"""
    frame_rate = 1/raw_clip.fps
    frame_chunks = raw_clip.audio.iter_chunks(chunk_duration=frame_rate)
    return tuple(np.max(chunk) for chunk in frame_chunks)

def find_strikes(max_frame_audio, threshold,  fps) -> tuple:
    """Return time (s) of each strike"""
    hit_frames, _ = find_peaks(max_frame_audio, height=threshold, distance=5*fps)
    hit_sec = tuple(hf/fps for hf in hit_frames)
    return hit_sec

def get_shot_times(strikes, pre_strike, post_strike) -> tuple:
    """Returns a nested tuple containing the start, end time of each shot"""
    return tuple((s-pre_strike, s+post_strike) for s in strikes)

def export_shots(raw_clip, shot_times, base_name, out_dir=None) -> None:
    """Exports clips to desired directory"""
    out_dir = DEFAULT_OUT if out_dir is None else Path(out_dir)
    
    print(f'Exporting {len(shot_times)} shots...')
    
    for i, (start, end) in enumerate(shot_times, start=1):
        filepath = out_dir / f'{base_name}_{i}.mp4'
        shot = raw_clip.subclip(start, end)
        shot.write_videofile(filepath)
    return None

if __name__ == '__main__':
    
    clip_filepath = f'{CLIP_DIR}/{CLIP_NAME}'
    clip_stem = Path(CLIP_NAME).stem

    clip = mpy.VideoFileClip(clip_filepath,target_resolution=(1920, 1080))

    frame_audio = get_max_frame_audio(clip)
    strikes = find_strikes(frame_audio, HIT_THRESHOLD, clip.fps)
    shot_times = get_shot_times(strikes, PRE_STRIKE, POST_STRIKE)

    export_shots(clip, shot_times, clip_stem)