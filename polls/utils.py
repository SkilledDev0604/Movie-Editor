from moviepy.editor import *
from django.conf import settings
from datetime import datetime
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import ffmpeg
import subprocess
import cv2
import numpy as np
from vidgear.gears import CamGear


def get_position(t, frames, size):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return (10000, 10000), (10000, 10000)
    if i == 0:
        return (10000, 10000), (10000, 10000)
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
        (frames[i - 1]["x"], frames[i - 1]["y"]),
        (frames[i]["x"], frames[i]["y"]),
        frames[i - 1]["time"],
        frames[i]["time"],
        frames[i - 1]["size"],
        frames[i]["size"],
        frames[i - 1]["angle"],
        frames[i]["angle"],
    )
    time = (t - time_from) / (time_to - time_from)
    angle = math.radians((angle_to - angle_from) * time + angle_from)
    width, height = size
    # width = abs(size[0] * math.cos(angle)) + abs(size[1] * math.sin(angle))
    # height = abs(size[0] * math.sin(angle)) + abs(size[1] * math.cos(angle))
    text_position = (
            position_from[0] + (position_to[0] - position_from[0]) * time - width * 0.5,
            position_from[1] + (position_to[1] - position_from[1]) * time - height * 0.5
        )
    text_center = (
            position_from[0] + (position_to[0] - position_from[0]) * time,
            position_from[1] + (position_to[1] - position_from[1]) * time
        )
    return (text_position, text_center)

def get_text_size(text, font_file, fontsize):
    font = ImageFont.truetype(font_file, fontsize)
    return font.getsize(text)


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
    return angle

def get_scale(t, frames):
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
    return scale


def make_video_1(form, image_file=None):
    videodir = f"{settings.BASE_DIR}\\static\\videos\\PawPatrolVideoInvitaion\\"
    input_file = videodir + "basic.mp4"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    output_file = f"{videodir}output_{now}.mp4"
    
    font_file = f"{settings.BASE_DIR}\\static\\fonts\\Aachen BT Bold font.ttf"
    

    # Open video stream
    stream = CamGear(source=input_file).start()

    # Get length of video
    duration = VideoFileClip(input_file).duration

    # Define the text properties
    text = "Hello, World!"

    # Define output video writer
    output_path = output_file
    output_fps = stream.framerate
    output_height, output_width = stream.frame.shape[:2]
    fourcc = cv2.VideoWriter.fourcc(*'H264')
    output_video = cv2.VideoWriter(output_path, fourcc, output_fps, (output_width, output_height))

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
            "stroke_color": "black",
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
    y = 0.4 * height
    x = width / 2 + delta_x
    text_objects.append(
        {
            "text": f"{form['linea4']}",
            "fontsize": 150,
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
    x= 0.5 * width + delta_x
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
                {
                    "time": duration - 0.1,
                    "x": x,
                    "y": y,
                    "size": 1,
                    "angle": 0,
                },
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
                {
                    "time": duration - 0.1,
                    "x": x,
                    "y": y,
                    "size": 1,
                    "angle": 0,
                },
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
                {
                    "time": duration - 0.1,
                    "x": x,
                    "y": y,
                    "size": 1,
                    "angle": 0,
                },
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
                {
                    "time": duration - 0.1,
                    "x": x,
                    "y": y,
                    "size": 1,
                    "angle": 0,
                },
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
                {
                    "time": duration - 0.1,
                    "x": x,
                    "y": y,
                    "size": 1,
                    "angle": 0,
                },
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
                {"time": duration - 0.1, "x": x, "y": y, "size": 1, "angle": 0, },
                {"time": duration, "x": x, "y": y, "size": 0.1, "angle": 0, },
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
        ratio = widht_ratio if height_ratio < widht_ratio else height_ratio
        y = 0.2 * height
        delta_x = 20
        image_objects.append({
            "ratio": ratio,
            "frames" : (
                {"time": 4, "x": 0.5 * width - delta_x, "y": y, "size": 1, "angle": 0},
                {"time": 4.5, "x": 0.5 * width - delta_x, "y": y, "size": 1, "angle": 0},
                {"time": 10, "x": 0.5 * width + delta_x, "y": y, "size": 1, "angle": 0},
            ),
            "angle": 0
        })
        x = 0.75 * width
        y = 0.5 * height
        image_objects.append({
            "ratio": ratio,
            "frames" : (
                {"time": 11.5, "x": x, "y": y, "size": 0.5, "angle": 0},
                {"time": 11.6, "x": x, "y": y, "size": 1.2, "angle": 0},
                {"time": 11.7, "x": x, "y": y, "size": 1, "angle": 0},
                {"time": duration, "x": x, "y": y, "size": 1, "angle": 0},
            ),
            "angle": 0
        })

    for text_object in text_objects:
        font = ImageFont.truetype(text_object['font_file'], size=round(text_object['fontsize']))
        if text_object['radius'] != 0:
            text_object['image'] = get_curved_text(text= text_object['text'], font=font, color=text_object['color'], stroke_color=text_object['stroke_color'], stroke_width=text_object['stroke_width'], height=height, width=width, radius=text_object['radius'])
        else:
            bg = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            d = ImageDraw.Draw(bg)
            # Get size of text box 
            size = d.textsize(text_object['text'], font)
            d.text((bg.size[0]/2-size[0]/2, bg.size[1]/2-size[1]/2), text_object['text'], fill=text_object['color'], font=font, stroke_fill=text_object['stroke_color'], stroke_width=text_object['stroke_width'], align='center')
            text_object['image'] = bg
    count = 0
    while True:
        
        # Read frames from the video stream
        frame = stream.read()

        # Break the loop if the video has ended
        if frame is None:
            break
        time = count / stream.framerate
        print(time)
        count += 1
        # Create a blank canvas with the same size as the frame
        pil_frame = Image.fromarray(frame).convert('RGB')

        for image_object in image_objects:
            resized_image = image.resize((round(image.size[0] * ratio * (image_object['ratio'])), round(image.size[1] * ratio * image_object['ratio'])))
            rotated_image = resized_image.rotate(get_angle(time, image_object['frames']))
            pos, _ = get_position(time, image_object['frames'], rotated_image.size)
            b, g, r = rotated_image.split()
            converted_image = Image.merge("RGB", (r, g, b))
            pil_frame.paste(converted_image, (round(pos[0]), round(pos[1])))

        # Create a drawing object
        draw = ImageDraw.Draw(pil_frame)

        for text_object in text_objects:
            # Specify the text content and position
            text = text_object['text']
            # Get size of text box 
            size = draw.textsize(text, font)
            size = (size[0], size[1]+len(text_object['text'].split('\n'))*10)
            # Get angle of text
            angle = get_angle(time, text_object['frames'])
            # Get position of text box
            (text_position, text_center) = get_position(t=time, frames=text_object['frames'], size=size)
            # Draw the text on the image
            scale = get_scale(time, text_object['frames'])
            bg = text_object['image'].resize((round(text_object['image'].size[0] * scale), round(text_object['image'].size[1] * scale)), resample = Image.BICUBIC)
            bg = bg.rotate(angle, fillcolor="#00000000")
            pil_frame.paste(bg, (round(text_center[0]-bg.size[0]/2), round(text_center[1]-bg.size[1]/2)), bg)


                
        # Convert the modified PIL Image back to OpenCV format
        modified_frame = np.array(pil_frame)

        output_video.write(modified_frame)
     
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    output_video.release()
    cv2.destroyAllWindows()
    stream.stop()
    return f"videos/PawPatrolVideoInvitaion/output_{now}.mp4"


def get_curved_text(text, font, color, stroke_color, stroke_width, width, height, radius):
    bg = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    d = ImageDraw.Draw(bg)
    all_width = 0
    for character in text:
        all_width += d.textsize(character, font)[0]
    sum_width = 0
    for character in text:
        size = d.textsize(character, font)
        length = all_width / 2 - sum_width - size[0] / 2
        sum_width += size[0]
        angle = length / radius
        delta_x = -radius * math.sin(angle)
        delta_y = radius - radius * math.cos(angle)
        ch_image = Image.new("RGBA", (width * 2, height * 2), (255, 255, 255, 0))
        ch_d = ImageDraw.Draw(ch_image)
        ch_d.text((ch_image.size[0]/2-size[0]/2, ch_image.size[1]/2-size[1]/2), character, fill=color, font=font, stroke_fill=stroke_color, stroke_width=stroke_width, align='center')
        ch_image = ch_image.rotate(math.degrees(angle), fillcolor="#00000000", resample=Image.BICUBIC)
        bg.paste(ch_image, (round(bg.size[0]/2 + delta_x - ch_image.size[0]/2), round(bg.size[1]/2 + delta_y - ch_image.size[1]/2)), ch_image)
    return bg
