from moviepy.editor import *
from django.conf import settings
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_objects(form, image_file):
    videodir = f"{settings.BASE_DIR}/static/videos/PawPatrolVideoInvitaion/"
    input_file = videodir + "basic.mp4"
    # input_file = videodir + "basic_hd.mp4"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    output_file = f"{videodir}output_{now}.mp4"

    font_file = f"{settings.BASE_DIR}/static/fonts/Aachen BT Bold font.ttf"

    # Get length of video
    video_clip = VideoFileClip(input_file)
    duration = video_clip.duration
    output_width, output_height = video_clip.size

    text_objects = []
    width = output_width
    height = output_height

    x = 0.5 * width
    y = 0.15 * height
    text_objects.append(
        {
            "text": f"{form['linea1']}\n{form['linea2']}\n{form['linea3']}",
            "fontsize": 70,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 5,
            "stroke_color": "#a9a9a9",
            "frames": (
                {"time": 0, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 3.8, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 3.9, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 4, "x": x, "y": y, "size": 0.1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # BEN
    delta_x = -10
    delta_y = (1 - 3/len(form['linea4'])) * height * 0.1
    y = 0.4 * height + delta_y
    x = width / 2 + delta_x
    text_objects.append(
        {
            "text": f"{form['linea4']}",
            "fontsize": 150 / len(form['linea4']) * 3,
            "font_file": font_file,
            "color": "#871E25",
            "stroke_width": 8,
            "stroke_color": "white",
            "frames": (
                {"time": 5, "x": x, "y": y + 200, "size": 1, "angle": 0},
                {"time": 5.25, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 10.75, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 11, "x": x, "y": y - 200, "size": 1, "angle": 0},
            ),
            "radius": 400,
        }
    )

    # IS TUNING
    delta_x = -10
    y = 0.55 * height
    x = 0.5 * width + delta_x
    text_objects.append(
        {
            "text": f"{form['linea5']}",
            "fontsize": 35,
            "font_file": font_file,
            "color": "#871E25",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": 5.5, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 5.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 5.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 10.8, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": 10.9, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 11, "x": x, "y": y, "size": 0.1, "angle": 0},
            ),
            "radius": 400,
        }
    )

    # 2
    delta_x = -10
    y = 0.75 * height
    text_objects.append(
        {
            "text": f"{form['linea6']}",
            "fontsize": 250,
            "font_file": font_file,
            "color": "#DFC00C",
            "stroke_width": 10,
            "stroke_color": "white",
            "frames": (
                {"time": 6, "x": width, "y": y, "size": 1, "angle": -30},
                {"time": 6.2, "x": 0.5 * width, "y": y, "size": 1, "angle": 0},
                {"time": 10.8, "x": 0.5 * width, "y": y, "size": 1, "angle": -110},
                {"time": 11, "x": 0.5 * width, "y": height, "size": 1, "angle": -45},
            ),
            "radius": 0,
        }
    )

    # 2:00-5:00PM SUNDAY DECEMBER
    y = 0.04 * height
    text_objects.append(
        {
            "text": f"{form['linea7']}",
            "fontsize": 25,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": 11.5, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 11.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 11.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    y = 0.08 * height
    text_objects.append(
        {
            "text": f"{form['linea8']}",
            "fontsize": 50,
            "font_file": font_file,
            "color": "#b5b823",
            "stroke_width": 5,
            "stroke_color": "white",
            "frames": (
                {"time": 11.5, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 11.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 11.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    y = 0.13 * height
    text_objects.append(
        {
            "text": f"{form['linea9']}",
            "fontsize": 25,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": 11.5, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 11.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 11.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # RSVP TO MOM +657
    y = 0.2 * height
    text_objects.append(
        {
            "text": f"{form['linea10']}",
            "fontsize": 40,
            "font_file": font_file,
            "color": "#871E25",
            "stroke_width": 2,
            "stroke_color": "white",
            "frames": (
                {"time": 12, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 12.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 12.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    y = 0.25 * height
    text_objects.append(
        {
            "text": f"{form['linea11']}",
            "fontsize": 40,
            "font_file": font_file,
            "color": "#DFC00C",
            "stroke_width": 2,
            "stroke_color": "white",
            "frames": (
                {"time": 12, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 12.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 12.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    y = 0.36 * height
    text_objects.append(
        {
            "text": f"{form['linea12']}\n{form['linea13']}",
            "fontsize": 25,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": 12.5, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": 12.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 12.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration, "x": x, "y": y, "size": 0.1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    image_objects = []
    image = None
    if image_file:
        image = Image.open(image_file)
        # Trim the transparent parts
        image = image.crop(image.getbbox())
        height_ratio = 0.3 * height / image.size[1]
        widht_ratio = width / image.size[0]
        ratio = height_ratio if height_ratio < widht_ratio else widht_ratio
        y = 0.2 * height
        delta_x = 20
        image_objects.append(
            {
                "ratio": ratio,
                "frames": (
                    {"time": 4,"x": 0.5 * width - delta_x,"y": y,"size": 1,"angle": 0},
                    {"time": 4.5,"x": 0.5 * width - delta_x,"y": y,"size": 1,"angle": 0},
                    {"time": 10,"x": 0.5 * width + delta_x,"y": y,"size": 1,"angle": 0},
                ),
                "angle": 0,
            }
        )
        x = 0.75 * width
        y = 0.5 * height
        image_objects.append(
            {
                "ratio": ratio,
                "frames": (
                    {"time": 11.5, "x": x, "y": y, "size": 0.5, "angle": 0},
                    {"time": 11.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                    {"time": 11.7, "x": x, "y": y, "size": 1, "angle": 0},
                    {"time": duration, "x": x, "y": y, "size": 1, "angle": 0},
                ),
                "angle": 0,
            }
        )

    return (input_file, output_file, now, text_objects, image_objects)
