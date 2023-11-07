from moviepy.editor import *
from django.conf import settings
from datetime import datetime


def get_position(t, frames, size):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return frames[-1]["position"]
    if i == 0:
        return frames[0]["position"]
    position_from, position_to, time_from, time_to, size_from, size_to = (
        frames[i - 1]["position"],
        frames[i]["position"],
        frames[i - 1]["time"],
        frames[i]["time"],
        frames[i - 1]["size"],
        frames[i]["size"],
    )
    time = (t - time_from) / (time_to - time_from)
    # print('\n', t, position_from[1] + (position_to[1] - position_from[1]) * (t - time_from) / (time_to - time_from))
    return (
        position_from[0]
        + (position_to[0] - position_from[0]) * time - size[0] * 0.5 * ((size_to - size_from) * time + size_from),
        position_from[1]
        + (position_to[1] - position_from[1]) * time - size[1] * 0.5 * ((size_to - size_from) * time + size_from),
    )


def get_size(t, frames, size):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return frames[-1]["size"]
    if i == 0:
        return frames[0]["size"]
    size_from, size_to, time_from, time_to = (
        frames[i - 1]["size"],
        frames[i]["size"],
        frames[i - 1]["time"],
        frames[i]["time"],
    )
    scale = size_from + (size_to - size_from) * (t - time_from) / (time_to - time_from)
    # print(size, scale)
    return (size[0] * scale, size[1] * scale)


def set_frames(clip, frames):
    print(frames[-1]["time"])
    duration = frames[-1]["time"] - frames[0]["time"]
    clip = clip.set_start(frames[0]["time"]).set_end(frames[-1]["time"])
    print(clip.duration)
    clip = clip.set_position(lambda t: get_position(t + frames[0]["time"], frames, size))
    size = clip.size
    clip = clip.resize(lambda t: get_size(t + frames[0]["time"], frames, size))
    return clip


def make_video_1(form):
    videodir = f"{settings.BASE_DIR}/static/videos/PawPatrolVideoInvitaion/"
    # Load the video file
    video_file = VideoFileClip(videodir + "basic.mp4")
    clips = [video_file]

    # Get the width and height of the video
    width, height = video_file.size

    # Create the text clip with animation
    text_clip = TextClip(
        f"{form['linea1']}\n{form['linea2']}\n{form['linea3']}",
        font="Arial-Bold",
        fontsize=150,
        color="white",
        stroke_color="Grey",
        stroke_width=4
    )
    clip_width, clip_height = text_clip.size

    frames = (
        {"time": 0, "position": (0.5 * width, 0.15 * height), "size": 0.1, "angle": 0},
        {
            "time": 0.1,
            "position": (
                0.5 * width,
                0.15 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {
            "time": 0.2,
            "position": (
                0.5 * width,
                0.15 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 3.8,
            "position": (
                0.5 * width,
                0.15 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 3.9,
            "position": (
                0.5 * width,
                0.15 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {"time": 4, "position": (0.5 * width, 0.15 * height), "size": 0.1, "angle": 0}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    text_clip = TextClip(
        f"{form['linea4']}",
        font="Arial-Bold",
        fontsize=355,
        color="#251E87",
        stroke_color="white",
        stroke_width=8
    )
    clip_width, clip_height = text_clip.size
    delta_x = -30
    y = 0.4 * height
    frames = (
        {
            "time": 5,
            "position": (
                width/2 + delta_x,
                y + 200
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 5.25,
            "position": (
                width/2 + delta_x,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 10.75,
            "position": (
                width/2 + delta_x,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 11,
            "position": (
                width/2 + delta_x,
                y - 200
            ),
            "size": 1,
            "angle": 0
        }
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # IS TUNING
    text_clip = TextClip(
        f"{form['linea5']}", font="Arial-Bold", fontsize=100, color="#251E87"
    )
    clip_width, clip_height = text_clip.size
    delta_x = -30
    frames = (
        {"time": 5.5, "position": (0.5 * width + delta_x, 0.5 * height), "size": 0.1},
        {
            "time": 5.6,
            "position": (
                0.5 * width + delta_x,
                0.5 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {
            "time": 5.7,
            "position": (
                0.5 * width + delta_x,
                0.5 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 10.8,
            "position": (
                0.5 * width + delta_x,
                0.5 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 10.9,
            "position": (
                0.5 * width + delta_x,
                0.5 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {"time": 11, "position": (0.5 * width + delta_x, 0.5 * height), "size": 0.1}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    
    # 2
    text_clip = TextClip(
        f"{form['linea6']}", font="Arial-Bold", fontsize=700, color="#0CC0DF", stroke_color="white", stroke_width=10
    )
    clip_width, clip_height = text_clip.size
    delta_x = -30
    y = 0.7 * height
    frames = (
        {"time": 6, "position": (width, y), "size": 0.1, "angle": -30},
        {
            "time": 6.2,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": 10.8,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": -70
        },
        {"time": 11, "position": (0.5 * width, height), "size": 1, "angle": -45}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    #2:00-5:00PM SUNDAY DECEMBER
    bg_clip = ColorClip(
        (round(video_file.w), round(video_file.h * 0.8)), color=(0,0,0,0), duration=12
    )
    text_clip1 = TextClip(
        f"{form['linea7']}", font="Arial-Bold", fontsize=60, color="white"
    )
    text_clip2 = TextClip(
        f"{form['linea8']}", font="Arial-Bold", fontsize=120, color="#0CC0DF00", stroke_color="white", stroke_width=5
    )
    text_clip3 = TextClip(
        f"{form['linea9']}", font="Arial-Bold", fontsize=60, color="white"
    )
    text_clip1 = text_clip1.set_position((bg_clip.w/2 - text_clip1.w/2, bg_clip.h/2 - text_clip2.h/2 + 30 - text_clip1.h))
    text_clip2 = text_clip2.set_position((bg_clip.w/2 - text_clip2.w/2, bg_clip.h/2 - text_clip2.h/2))
    text_clip3 = text_clip3.set_position((bg_clip.w/2 - text_clip3.w/2, bg_clip.h/2 + text_clip2.h/2 - 20))
    text_clip = CompositeVideoClip([bg_clip, text_clip1, text_clip2, text_clip3])
    clip_width, clip_height = text_clip.size
    y = 0.08 * height
    frames = (
        {"time": 11.5, "position": (0.5 * width, y), "size": 0.1},
        {
            "time": 11.6,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1.2,
            "angle": 0
        },
        {
            "time": 11.7,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.2,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.1,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1.2,
            "angle": 0
        },
        {"time": video_file.duration, "position": (0.5 * width, y), "size": 0.1}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)


    # RSVP TO MOM +657
    bg_clip = ColorClip(
        (round(video_file.w), round(video_file.h * 0.8)), color=(0,0,0,0), duration=12
    )
    text_clip1 = TextClip(
        f"{form['linea10']}", font="Arial-Bold", fontsize=80, color="#251E87", stroke_color="white", stroke_width=2
    )
    text_clip2 = TextClip(
        f"{form['linea11']}", font="Arial-Bold", fontsize=80, color="#0CC0DF", stroke_color="white", stroke_width=2
    )
    text_clip1 = text_clip1.set_position((bg_clip.w/2 - text_clip1.w/2, bg_clip.h/2 - text_clip1.h + 5))
    text_clip2 = text_clip2.set_position((bg_clip.w/2 - text_clip2.w/2, bg_clip.h/2 -5))
    text_clip = CompositeVideoClip([bg_clip, text_clip1, text_clip2])
    clip_width, clip_height = text_clip.size
    y = 0.2 * height
    frames = (
        {"time": 12, "position": (0.5 * width, y), "size": 0.1},
        {
            "time": 12.1,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1.2,
            "angle": 0
        },
        {
            "time": 12.2,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.2,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.1,
            "position": (
                0.5 * width,
                y
            ),
            "size": 1.2,
            "angle": 0
        },
        {"time": video_file.duration, "position": (0.5 * width, y), "size": 0.1}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    text_clip = TextClip(
        f"{form['linea12']}\n{form['linea13']}",
        font="Arial-Bold",
        fontsize=50,
        color="black"
    )

    frames = (
        {"time": 12.5, "position": (0.5 * width, 0.3 * height), "size": 0.1, "angle": 0},
        {
            "time": 12.6,
            "position": (
                0.5 * width,
                0.3 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {
            "time": 12.7,
            "position": (
                0.5 * width,
                0.3 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.2,
            "position": (
                0.5 * width,
                0.3 * height
            ),
            "size": 1,
            "angle": 0
        },
        {
            "time": video_file.duration - 0.1,
            "position": (
                0.5 * width,
                0.3 * height
            ),
            "size": 1.2,
            "angle": 0
        },
        {"time": video_file.duration, "position": (0.5 * width, 0.3 * height), "size": 0.1, "angle": 0}
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)
    

    # Overlay the text clip on the video
    final_clip = CompositeVideoClip(clips)

    # Write the final video file
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    final_clip.write_videofile(f"{videodir}output_{now}.mp4")

    return f"videos/PawPatrolVideoInvitaion/output_{now}.mp4"
