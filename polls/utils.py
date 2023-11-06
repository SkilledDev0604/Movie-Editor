from moviepy.editor import *
from django.conf import settings
from datetime import datetime

def set_move(clip, start_at, end_at, from_position, to_position):
    duration = end_at - start_at
    clip = clip.set_position(
        lambda t: 
        (
            (to_position[0] - from_position[0])  * (t - start_at) / duration + from_position[0], 
            (to_position[1] - from_position[1]) * (t - start_at) / duration + from_position[1]
        )).set_duration(end_at - start_at).set_start(start_at)
    return clip

def set_pop(clip, start_at, end_at, center_position, from_size, to_size, large_size):
    duration = end_at - start_at
    clip = clip.resize(lambda t: (t - start_at) / duration * (to_size - from_size) / from_size + 1).set_start(start_at)
    clip = clip.set_position()
    return clip

def get_position(t, frames):
    i = 0
    while i < len(frames) and t > frames[i]['time']: i += 1
    if i >= len(frames): return frames[-1]['position']
    if i == 0: return frames[0]['position']
    position_from, position_to, time_from, time_to = frames[i-1]['position'], frames[i]['position'], frames[i-1]['time'], frames[i]['time']
    return (
        position_from[0] + (position_to[0] - position_from[0]) * (t - time_from) / (time_to - time_from),
        position_from[1] + (position_to[1] - position_from[1]) * (t - time_from) / (time_to - time_from)
        )
        

def get_size(t, frames, size):
    i = 0
    while i < len(frames) and t > frames[i]['time']: i += 1
    if i >= len(frames): return frames[-1]['size']
    if i == 0: return frames[0]['size']
    size_from, size_to, time_from, time_to = frames[i-1]['size'], frames[i]['size'], frames[i-1]['time'], frames[i]['time']
    scale = size_from + (size_to - size_from) * (t - time_from) / (time_to - time_from)
    # print(size, scale)
    return (size[0] * scale, size[1] * scale)


def set_frames(clip, frames):
    print(clip.size)
    duration = frames[-1]['time'] - frames[0]['time']
    clip = clip.set_start(frames[0]['time']).set_end(frames[-1]['time'])
    clip = clip.set_position(lambda t: get_position(t, frames))
    size = clip.size
    clip = clip.resize(lambda t: get_size(t, frames, size))
    return clip


def make_video_1(form):
    videodir = f'{settings.BASE_DIR}/static/videos/PawPatrolVideoInvitaion/'
    # Load the video file
    video_file = VideoFileClip(videodir + 'basic.mp4')

    # Get the width and height of the video
    width, height = video_file.size

    # Create the text clip with animation
    text_clip1 = TextClip(f"{form['linea1']}\n{form['linea2']}\n{form['linea3']}", font='Arial-Bold', fontsize=150, color='white', stroke_color='Grey', stroke_width=4)
    clip_width, clip_height = text_clip1.size
    frames = (
        {'time':0, 'position': (0.5 * width, 0.15 * height), 'size': 0.1},
        {'time':0.1, 'position': (0.5 * width - 0.5 * clip_width * 1.2, 0.15 * height - 0.5 * clip_height * 1.2), 'size': 1.2},
        {'time':0.2, 'position': (0.5 * width - 0.5 * clip_width, 0.15 * height - 0.5 * clip_height), 'size': 1},
        {'time':3.8, 'position': (0.5 * width - 0.5 * clip_width, 0.15 * height - 0.5 * clip_height), 'size': 1},
        {'time':3.9, 'position': (0.5 * width - 0.5 * clip_width * 1.2, 0.15 * height - 0.5 * clip_height * 1.2), 'size': 1.2},
        {'time':4, 'position': (0.5 * width, 0.15 * height), 'size': 0.1},
        )
    text_clip1 = set_frames(text_clip1, frames)
    # Overlay the text clip on the video
    final_clip = CompositeVideoClip([video_file, text_clip1])

    # Write the final video file
    now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    final_clip.write_videofile(f'{videodir}output_{now}.mp4')
    print(f'{videodir}output_{now}.mp4')
