from moviepy.editor import *
from django.conf import settings
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_objects(form, image_file):
    videodir = f"{settings.BASE_DIR}/static/videos/Batman/"
    input_file = videodir + "basic.mp4"
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

    # join us to celebrate
    x = 0.5 * width
    y = 0.11 * height
    start = 0.4
    end = 2.2
    text_objects.append(
        {
            "text": f"{form['linea1']}",
            "fontsize": 18,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 0,
            "stroke_color": "orange",
            "frames": (
                {"time": start, "x": (1 - 0.2) * x, "y": y, "size": 1, "angle": 0},
                {"time": start+0.3, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.3, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": (1 + 0.2) * x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # ky'zien
    delta_x = -0.10
    y = 0.16 * height
    x = width / 2 + delta_x
    start = 3
    end = 5
    text_objects.append(
        {
            "text": f"{form['linea2']}",
            "fontsize": 50,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": start, "x": x, "y": y + 100, "size": 1, "angle": 0},
                {"time": start+0.3, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.3, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y - 100, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # IS TUNING
    delta_x = 0
    y = 0.33 * height
    x = 0.5 * width + delta_x
    start = 3.2
    end = 5.2
    text_objects.append(
        {
            "text": f"{form['linea3']}",
            "fontsize": 35,
            "font_file": font_file,
            "color": "white",
            "stroke_width": 0,
            "stroke_color": "white",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 0.1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # 5
    delta_x = 0
    x = 0.5 * width
    y = 0.48 * height
    start = 3.5
    end = 5.2
    text_objects.append(
        {
            "text": f"{form['linea4']}",
            "fontsize": 180,
            "font_file": font_file,
            "color": "Black",
            "stroke_width": 10,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": start + 0.5, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end - 0.5, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # SATURDAY
    y = 0.07 * height
    start = 6.1
    delta_time = 0.7
    end = 12
    text_objects.append(
        {
            "text": f"{form['linea5']}",
            "fontsize": 40,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # november 18
    y = 0.12 * height
    start += delta_time
    end = 12
    text_objects.append(
        {
            "text": f"{form['linea6']}",
            "fontsize": 20,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # 's house'
    y = 0.21 * height
    start += delta_time
    end = 12
    text_objects.append(
        {
            "text": f"{form['linea7']}",
            "fontsize": 30,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # 3152 ~ florida
    y = 0.28 * height
    start += delta_time
    end = 12
    text_objects.append(
        {
            "text": f"{form['linea8']}\n{form['linea9']}",
            "fontsize": 15,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    # rsvp to mom
    y = 0.38 * height
    start += delta_time * 2
    end = 12
    text_objects.append(
        {
            "text": f"{form['linea10']}\n{form['linea11']}",
            "fontsize": 30,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "radius": 0,
        }
    )

     # see you there
    y = 0.75 * height
    start = 13.2
    end = duration
    text_objects.append(
        {
            "text": f"{form['linea12']}",
            "fontsize": 40,
            "font_file": font_file,
            "color": "black",
            "stroke_width": 1,
            "stroke_color": "#00eeff",
            "frames": (
                {"time": start, "x": x, "y": y, "size": 0.1, "angle": 0},
                {"time": start+0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": start+0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.2, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": end-0.1, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": end, "x": x, "y": y, "size": 0.1, "angle": 0},
            ),
            "radius": 0,
        }
    )

    image_objects = []
    image = None
    if image_file:
        image = Image.open(image_file)
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
