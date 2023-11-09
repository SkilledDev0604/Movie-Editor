from moviepy.editor import *
from django.conf import settings
from datetime import datetime
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def get_curved_text_imageclip(
    text,
    font="arialbd",
    fontsize=70,
    color="white",
    stroke_color=None,
    stroke_width=0,
    radius=100,
    max_height=1000,
    max_width=1000,
):
    text_images = []
    width = 0
    font_path = f"{font}.ttf"
    font = ImageFont.truetype(font_path, fontsize)

    for character in text:
        text_width, text_height = font.getsize(character)
        width += text_width
        img = Image.new(
            "RGBA",
            (text_width + stroke_width * 2, text_height + stroke_width * 2),
            (0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(img)
        draw.text(
            (0, 0),
            character,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
        )
        text_images.append(img)
    sum_width = 0
    bg_image = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))
    all_images = [bg_image]

    for text_image in text_images:
        length = width / 2 - sum_width - text_image.width / 2
        sum_width += text_image.width
        angle = length / radius
        delta_x = -radius * math.sin(angle)
        delta_y = radius - radius * math.cos(angle)
        rotated_image = text_image.rotate(math.degrees(angle), expand=True)
        image_width, image_height = rotated_image.size
        position = (
            int(max_width / 2 + delta_x - image_width / 2),
            int(max_height / 2 + delta_y - image_height / 2),
        )
        bg_image.paste(rotated_image, position, rotated_image)
        all_images.append(bg_image)

    return ImageClip(np.array(bg_image))


def get_curved_text_clip(
    text,
    font="Arial-Bold",
    fontsize=70,
    color="white",
    stroke_color=None,
    stroke_width=0,
    radius=100,
    max_height=1000,
    max_width=1000,
    duration=20,
):
    text_clips = []
    width = 0
    for character in text:
        text_clip = TextClip(
            character,
            font=font,
            fontsize=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        text_clips.append(text_clip)
        width += text_clip.w
    sum_width = 0
    bg_clip = ColorClip((round(max_width), round(max_height)), color=(0, 0, 0, 0), duration=duration)
    all_clips = [bg_clip]
    for text_clip in text_clips:
        length = width / 2 - sum_width - text_clip.w / 2
        sum_width += text_clip.w
        angle = length / radius
        delta_x = -radius * math.sin(angle)
        delta_y = radius - radius * math.cos(angle)
        clip_width = abs(text_clip.w * math.cos(angle)) + abs(
            text_clip.h * math.sin(angle)
        )
        clip_height = abs(text_clip.w * math.sin(angle)) + abs(
            text_clip.h * math.cos(angle)
        )
        text_clip = text_clip.set_position(
            (
                max_width / 2 + delta_x - clip_width / 2,
                max_height / 2 + delta_y - clip_height / 2,
            )
        )
        text_clip = text_clip.rotate(math.degrees(angle), resample="bilinear")
        all_clips.append(text_clip)
    # videodir = f"{settings.BASE_DIR}/static/videos/PawPatrolVideoInvitaion/"
    # CompositeVideoClip(all_clips).write_videofile(f"{videodir}output0.mp4")
    return CompositeVideoClip(all_clips)


def get_position(t, frames, size):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return frames[-1]["position"]
    if i == 0:
        return frames[0]["position"]
    (
        position_from,
        position_to,
        time_from,
        time_to,
        size_from,
        size_to,
        angle_from,
        angle_to,
    ) = (
        frames[i - 1]["position"],
        frames[i]["position"],
        frames[i - 1]["time"],
        frames[i]["time"],
        frames[i - 1]["size"],
        frames[i]["size"],
        frames[i - 1]["angle"],
        frames[i]["angle"],
    )
    time = (t - time_from) / (time_to - time_from)
    angle = math.radians((angle_to - angle_from) * time + angle_from)
    width = abs(size[0] * math.cos(angle)) + abs(size[1] * math.sin(angle))
    height = abs(size[0] * math.sin(angle)) + abs(size[1] * math.cos(angle))
    return (
        position_from[0]
        + (position_to[0] - position_from[0]) * time
        - width * 0.5 * ((size_to - size_from) * time + size_from),
        position_from[1]
        + (position_to[1] - position_from[1]) * time
        - height * 0.5 * ((size_to - size_from) * time + size_from),
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


def get_angle(t, frames):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return frames[-1]["angle"]
    if i == 0:
        return frames[0]["angle"]
    angle_from, angle_to, time_from, time_to = (
        frames[i - 1]["angle"],
        frames[i]["angle"],
        frames[i - 1]["time"],
        frames[i]["time"],
    )
    angle = angle_from + (angle_to - angle_from) * (t - time_from) / (
        time_to - time_from
    )
    # print(size, scale)
    return angle

def get_opacity(t, frames):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        opacity = frames[-1].get("opacity")
        if opacity != None: return opacity
        else : return 1
    if i == 0:
        opacity = frames[0].get("opacity")
        if opacity != None: return opacity
        else : return 1
    opacity_from, opacity_to, time_from, time_to = (
        frames[i - 1]["opacity"],
        frames[i]["opacity"],
        frames[i - 1]["time"],
        frames[i]["time"],
    )
    if opacity_from == None: opacity_from = 1
    if opacity_to == None: opacity_to = 1
    opacity = opacity_from + (opacity_to - opacity_from) * (t - time_from) / (
        time_to - time_from
    )
    return opacity


def set_frames(clip, frames):
    duration = frames[-1]["time"] - frames[0]["time"]
    clip = clip.set_start(frames[0]["time"]).set_end(frames[-1]["time"])
    clip = clip.set_position(
        lambda t: get_position(t + frames[0]["time"], frames, size)
    )
    size = clip.size
    clip = clip.resize(lambda t: get_size(t + frames[0]["time"], frames, size))
    clip = clip.rotate(lambda t: get_angle(t + frames[0]["time"], frames))
    # clip = clip.set_opacity(lambda t: get_opacity(t + frames[0]["time"], frames))
    # clip = clip.fx(CompositeVideoClip, opacity=get_opacity)
    return clip


def make_video_1(form, image=None):
    videodir = f"{settings.BASE_DIR}/static/videos/PawPatrolVideoInvitaion/"
    # Load the video file
    video_file = VideoFileClip(videodir + "basic.mp4")
    # video_file = video_file.resize([video_file.w*2, video_file.h*2])
    clips = [video_file]

    # Get the width and height of the video
    width, height = video_file.size

    if image:
        image_clip = ImageClip(image)
        height_ratio = 0.3 * height / image_clip.h
        widht_ratio = width / image_clip.w
        if height_ratio < widht_ratio:
            image_clip = image_clip.resize(
                (image_clip.w * height_ratio, image_clip.h * height_ratio)
            )
        else:
            image_clip = image_clip.resize(
                (image_clip.w * widht_ratio, image_clip.h * widht_ratio)
            )
        y = 0.2 * height
        delta_x = 20
        frames = (
            {"time": 4, "position": (0.5 * width - delta_x, y), "size": 1, "angle": 0, 'opacity':0},
            {"time": 4.5, "position": (0.5 * width - delta_x, y), "size": 1, "angle": 0},
            {"time": 10, "position": (0.5 * width + delta_x, y), "size": 1, "angle": 0},
        )
        image_clip = set_frames(image_clip, frames)
        clips.append(image_clip)
        x = 0.75 * width
        y = 0.5 * height
        frames = (
            {"time": 11.5, "position": (0.5 * width, y), "size": 0.5, "angle": 0},
            {"time": 11.6, "position": (x, y), "size": 1.2, "angle": 0},
            {"time": 11.7, "position": (x, y), "size": 1, "angle": 0},
            {"time": video_file.duration, "position": (x, y), "size": 1, "angle": 0},
        )
        image_clip = set_frames(image_clip, frames)
        clips.append(image_clip)

    # Create the text clip with animation
    text_clip = TextClip(
        f"{form['linea1']}\n{form['linea2']}\n{form['linea3']}",
        font="Arial-Bold",
        fontsize=70,
        color="white",
        stroke_color="Grey",
        stroke_width=2,
    )
    clip_width, clip_height = text_clip.size

    frames = (
        {"time": 0, "position": (0.5 * width, 0.15 * height), "size": 0.1, "angle": 0},
        {
            "time": 0.1,
            "position": (0.5 * width, 0.15 * height),
            "size": 1.2,
            "angle": 0,
        },
        {"time": 0.2, "position": (0.5 * width, 0.15 * height), "size": 1, "angle": 0},
        {"time": 3.8, "position": (0.5 * width, 0.15 * height), "size": 1, "angle": 0},
        {
            "time": 3.9,
            "position": (0.5 * width, 0.15 * height),
            "size": 1.2,
            "angle": 0,
        },
        {"time": 4, "position": (0.5 * width, 0.15 * height), "size": 0.1, "angle": 0},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # BEN
    text_clip = get_curved_text_clip(
        f"{form['linea4']}",
        font="Arial-Bold",
        fontsize=150,
        color="#251E87",
        stroke_color="white",
        stroke_width=8,
        max_width=video_file.w * 2,
        max_height=video_file.h * 2,
        radius=400,
    )
    clip_width, clip_height = text_clip.size
    delta_x = -10
    y = 0.45 * height
    frames = (
        {"time": 5, "position": (width / 2 + delta_x, y + 200), "size": 1, "angle": 0},
        {"time": 5.25, "position": (width / 2 + delta_x, y), "size": 1, "angle": 0},
        {"time": 10.75, "position": (width / 2 + delta_x, y), "size": 1, "angle": 0},
        {"time": 11, "position": (width / 2 + delta_x, y - 200), "size": 1, "angle": 0},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # IS TUNING
    text_clip = get_curved_text_clip(
        f"{form['linea5']}",
        font="Arial-Bold",
        fontsize=35,
        color="#251E87",
        radius=400,
        max_height=video_file.h,
        max_width=video_file.w,
    )
    clip_width, clip_height = text_clip.size
    delta_x = -10
    y = 0.55 * height
    frames = (
        {"time": 5.5, "position": (0.5 * width + delta_x, y), "size": 0.1, "angle": 0},
        {"time": 5.6, "position": (0.5 * width + delta_x, y), "size": 1.2, "angle": 0},
        {"time": 5.7, "position": (0.5 * width + delta_x, y), "size": 1, "angle": 0},
        {"time": 10.8, "position": (0.5 * width + delta_x, y), "size": 1, "angle": 0},
        {"time": 10.9, "position": (0.5 * width + delta_x, y), "size": 1.2, "angle": 0},
        {"time": 11, "position": (0.5 * width + delta_x, y), "size": 0.1, "angle": 0},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # 2
    text_clip = TextClip(
        f"{form['linea6']}",
        font="Arial-Bold",
        fontsize=250,
        color="#0CC0DF",
        stroke_color="white",
        stroke_width=10,
    )
    clip_width, clip_height = text_clip.size
    delta_x = -10
    y = 0.75 * height
    frames = (
        {"time": 6, "position": (width, y), "size": 0.1, "angle": -30},
        {"time": 6.2, "position": (0.5 * width, y), "size": 1, "angle": 0},
        {"time": 10.8, "position": (0.5 * width, y), "size": 1, "angle": -70},
        {"time": 11, "position": (0.5 * width, height), "size": 1, "angle": -45},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # 2:00-5:00PM SUNDAY DECEMBER
    bg_clip = ColorClip(
        (round(video_file.w), round(video_file.h * 0.8)),
        color=(0, 0, 0, 0),
        duration=12,
    )
    text_clip1 = TextClip(
        f"{form['linea7']}", font="Arial-Bold", fontsize=25, color="white"
    )
    text_clip2 = TextClip(
        f"{form['linea8']}",
        font="Arial-Bold",
        fontsize=50,
        color="#0CC0DF00",
        stroke_color="white",
        stroke_width=3,
    )
    text_clip3 = TextClip(
        f"{form['linea9']}", font="Arial-Bold", fontsize=25, color="white"
    )
    text_clip1 = text_clip1.set_position(
        (
            bg_clip.w / 2 - text_clip1.w / 2,
            bg_clip.h / 2 - text_clip2.h / 2 + 10 - text_clip1.h,
        )
    )
    text_clip2 = text_clip2.set_position(
        (bg_clip.w / 2 - text_clip2.w / 2, bg_clip.h / 2 - text_clip2.h / 2)
    )
    text_clip3 = text_clip3.set_position(
        (bg_clip.w / 2 - text_clip3.w / 2, bg_clip.h / 2 + text_clip2.h / 2 - 10)
    )
    text_clip = CompositeVideoClip([bg_clip, text_clip1, text_clip2, text_clip3])
    clip_width, clip_height = text_clip.size
    y = 0.08 * height
    frames = (
        {"time": 11.5, "position": (0.5 * width, y), "size": 0.1, "angle": 0},
        {"time": 11.6, "position": (0.5 * width, y), "size": 1.2, "angle": 0},
        {"time": 11.7, "position": (0.5 * width, y), "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "position": (0.5 * width, y),
            "size": 1,
            "angle": 0,
        },
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # RSVP TO MOM +657
    bg_clip = ColorClip(
        (round(video_file.w), round(video_file.h * 0.8)),
        color=(0, 0, 0, 0),
        duration=12,
    )
    text_clip1 = TextClip(
        f"{form['linea10']}",
        font="Arial-Bold",
        fontsize=40,
        color="#251E87",
        stroke_color="white",
        stroke_width=2,
    )
    text_clip2 = TextClip(
        f"{form['linea11']}",
        font="Arial-Bold",
        fontsize=40,
        color="#0CC0DF",
        stroke_color="white",
        stroke_width=2,
    )
    text_clip1 = text_clip1.set_position(
        (bg_clip.w / 2 - text_clip1.w / 2, bg_clip.h / 2 - text_clip1.h + 5)
    )
    text_clip2 = text_clip2.set_position(
        (bg_clip.w / 2 - text_clip2.w / 2, bg_clip.h / 2 - 5)
    )
    text_clip = CompositeVideoClip([bg_clip, text_clip1, text_clip2])
    clip_width, clip_height = text_clip.size
    y = 0.225 * height
    frames = (
        {"time": 12, "position": (0.5 * width, y), "size": 0.1, "angle": 0},
        {"time": 12.1, "position": (0.5 * width, y), "size": 1.2, "angle": 0},
        {"time": 12.2, "position": (0.5 * width, y), "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "position": (0.5 * width, y),
            "size": 1,
            "angle": 0,
        },
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    text_clip = TextClip(
        f"{form['linea12']}\n{form['linea13']}",
        font="Arial-Bold",
        fontsize=25,
        color="black",
    )
    y = 0.325 * height
    frames = (
        {"time": 12.5, "position": (0.5 * width, y), "size": 0.1, "angle": 0},
        {"time": 12.6, "position": (0.5 * width, y), "size": 1.2, "angle": 0},
        {"time": 12.7, "position": (0.5 * width, y), "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "position": (0.5 * width, y),
            "size": 1,
            "angle": 0,
        },
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # Overlay the text clip on the video
    final_clip = CompositeVideoClip(clips)

    # Write the final video file
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    final_clip.write_videofile(f"{videodir}output_{now}.mp4")

    return f"videos/PawPatrolVideoInvitaion/output_{now}.mp4"
