from moviepy.editor import *
from django.conf import settings
from datetime import datetime
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import subprocess
import cv2
import numpy as np
from vidgear.gears import CamGear
from .objects import (pawpatrol, batman)

def get_objects(index, form, image_file):
    if index == 1: return batman.get_objects(form=form, image_file=image_file)
    else: return pawpatrol.get_objects(form=form, image_file=image_file)

inputs = (
    (
        {"id":"1"},
        {"id":"1", "value": "JOIN US", "maxlength": 25, "required": True},
        {"id":"2", "value": "TO", "maxlength": 25, "required": True},
        {"id":"3", "value": "CELEBRATE!", "maxlength": 25, "required": True},
        {"id":"2"},
        {"id":"4", "value": "BEN", "maxlength": 25, "required": True},
        {"id":"5", "value": "IS TURNING", "maxlength": 25, "required": True},
        {"id":"6", "value": "2", "maxlength": 25, "required": True},
        {"id":"3"},
        {"id":"7", "value": "2:00-5:00PM", "maxlength": 25, "required": True},
        {"id":"8", "value": "SUNDAY", "maxlength": 25, "required": True},
        {"id":"9", "value": "DECEMBER", "maxlength": 25, "required": True},
        {"id":"10", "value": "PSVP TO MOM", "maxlength": 25, "required": True},
        {"id":"11", "value": "+657-278-990", "maxlength": 25, "required": True},
        {"id":"12", "value": "126, GREENVILE", "maxlength": 25, "required": True},
        {"id":"13", "value": "STREET 1, CA", "maxlength": 25, "required": True},
    ),
    (
        {"id":"1"},
        {"id":"1", "value": "JOIN US TO CELEBRATE", "maxlength": 25, "required": True},
        {"id":"2"},
        {"id":"2", "value": "KY'ZIEN", "maxlength": 25, "required": True},
        {"id":"3", "value": "IS TURNING", "maxlength": 25, "required": True},
        {"id":"4", "value": "5", "maxlength": 25, "required": True},
        {"id":"3"},
        {"id":"5", "value": "SATURDAY", "maxlength": 25, "required": True},
        {"id":"6", "value": "NOVEMBER 18", "maxlength": 25, "required": True},
        {"id":"7", "value": "KY'ZIEN'S HOUSE", "maxlength": 25, "required": True},
        {"id":"8", "value": "3152 CERRY TREE DRIVE,", "maxlength": 25, "required": True},
        {"id":"9", "value": "JACKSONVILLE, FLORIDA", "maxlength": 25, "required": True},
        {"id":"10", "value": "RSVP TO MOM", "maxlength": 25, "required": True},
        {"id":"11", "value": "+657-278-990", "maxlength": 25, "required": True},
        {"id":"4"},
        {"id":"12", "value": "SEE YOU THERE", "maxlength": 25, "required": True},
    ),
)

titles = ('Paw Patrol', "Batman")

samples = ('videos/PawPatrolVideoInvitaion/sample.mp4', 'videos/Batman/sample.mp4')


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
        position_from[1] + (position_to[1] - position_from[1]) * time - height * 0.5,
    )
    text_center = (
        position_from[0] + (position_to[0] - position_from[0]) * time,
        position_from[1] + (position_to[1] - position_from[1]) * time,
    )
    return (text_position, text_center)


def get_text_size(text, font_file, fontsize):
    font = ImageFont.truetype(font_file, fontsize)
    return font.getsize(text)


def set_bound(img, bound):
    draw = ImageDraw.Draw(img)
    delete_regions = []
    if bound[0] != 0:
        delete_regions.append((0, 0, bound[0] * img.size[0], img.size[1]))
    if bound[1] != 0:
        delete_regions.append((0, 0, img.size[0], bound[1] * img.size[1]))
    if bound[2] != 1:
        delete_regions.append((bound[2] * img.size[0], 0, img.size[0], img.size[1]))
    if bound[3] != 1:
        delete_regions.append((0, bound[3] * img.size[1], img.size[0], img.size[1]))
    for region in delete_regions:
        draw.rectangle(region, fill=(0, 0, 0, 0))
    return img

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

def get_bound(t, frames):
    i = 0
    while i < len(frames) and t > frames[i]["time"]:
        i += 1
    if i >= len(frames):
        return (0, 0, 1, 1)
    if i == 0:
        return (0, 0, 1, 1)
    bound_from, bound_to, time_from, time_to = (
        frames[i - 1].get('bound') if frames[i - 1].get('bound') else (0, 0, 1, 1),
        frames[i].get('bound') if frames[i].get('bound') else (0, 0, 1, 1),
        frames[i - 1]["time"],
        frames[i]["time"],
    )
    bound = [0, 0, 1, 1]
    for index, abound in enumerate(bound_from):
        bound[index] = abound + (bound_to[index] - abound) * (t - time_from) / (
            time_to - time_from
        )
    return bound


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


def make_video(index=0, form=None, image_file=None):
    if form is None:
        return
    input_file, output_file, now, text_objects, image_objects = get_objects(
        index, form=form, image_file=image_file
    )

    video_dirs = ('PawPatrolVideoInvitaion', 'Batman')

    temp_audio = f"temp/temp_{now}.mp3"
    temp_file = f"temp/temp_{now}.mp4"
    return_file = f"videos/{video_dirs[index]}/output_{now}.mp4"

    stream = CamGear(source=input_file).start()

    # Get length of video
    video_clip = VideoFileClip(input_file)

    # Get audio
    video_clip.audio.write_audiofile(temp_audio)

    # Define output video writer
    output_fps = stream.framerate
    output_height, output_width = stream.frame.shape[:2]
    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
    output_video = cv2.VideoWriter(
        temp_file, fourcc, output_fps, (output_width, output_height)
    )
    width = output_width
    height = output_height

    image = None

    if len(image_objects) > 0:
        image = Image.open(image_file)

    for text_object in text_objects:
        font = ImageFont.truetype(
            text_object["font_file"], size=round(text_object["fontsize"])
        )
        if text_object["radius"] != 0:
            text_object["image"] = get_curved_text(
                text=text_object["text"],
                font=font,
                color=text_object["color"],
                stroke_color=text_object["stroke_color"],
                stroke_width=text_object["stroke_width"],
                height=height,
                width=width,
                radius=text_object["radius"],
            )
        else:
            bg = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            d = ImageDraw.Draw(bg)
            # Get size of text box
            size = d.textsize(text_object["text"], font)
            d.text(
                (bg.size[0] / 2 - size[0] / 2, bg.size[1] / 2 - size[1] / 2),
                text_object["text"],
                fill=text_object["color"],
                font=font,
                stroke_fill=text_object["stroke_color"],
                stroke_width=text_object["stroke_width"],
                align="center",
            )
            text_object["image"] = bg
    count = 0
    printed_time = 0
    while True:
        # # Read frames from the video stream
        frame = stream.read()

        # Break the loop if the video has ended
        if frame is None:
            break
        time = count / stream.framerate
        if time - printed_time > 0.5: 
            print(time)
            printed_time = time
        count += 1
        # Create a blank canvas with the same size as the frame
        pil_frame = Image.fromarray(frame).convert("RGB")

        for image_object in image_objects:
            resized_image = image.resize(
                (
                    round(image.size[0]* image_object["ratio"]* get_scale(time, image_object["frames"])),
                    round(image.size[1]* image_object["ratio"]* get_scale(time, image_object["frames"])),
                )
            )
            rotated_image = resized_image.rotate(
                get_angle(time, image_object["frames"])
            )
            pos, _ = get_position(time, image_object["frames"], rotated_image.size)
            rotated_image = rotated_image.convert("RGB")
            b, g, r = rotated_image.split()
            converted_image = Image.merge("RGB", (r, g, b))
            pil_frame.paste(converted_image, (round(pos[0]), round(pos[1])))

        # Create a drawing object
        draw = ImageDraw.Draw(pil_frame)

        for text_object in text_objects:
            # Specify the text content and position
            text = text_object["text"]
            # Get size of text box
            size = draw.textsize(text, font)
            size = (size[0], size[1] + len(text_object["text"].split("\n")) * 10)
            # Get angle of text
            angle = get_angle(time, text_object["frames"])
            # Get position of text box
            (text_position, text_center) = get_position(
                t=time, frames=text_object["frames"], size=size
            )
            # Draw the text on the image
            scale = get_scale(time, text_object["frames"])
            bg = text_object["image"].resize(
                (
                    round(text_object["image"].size[0] * scale),
                    round(text_object["image"].size[1] * scale),
                ),
                resample=Image.BICUBIC,
            )
            bg = set_bound(bg, get_bound(time, text_object['frames']))
            bg = bg.rotate(angle, fillcolor="#00000000")

            pil_frame.paste(
                bg,
                (
                    round(text_center[0] - bg.size[0] / 2),
                    round(text_center[1] - bg.size[1] / 2),
                ),
                bg,
            )

        # Convert the modified PIL Image back to OpenCV format
        modified_frame = np.array(pil_frame)

        output_video.write(modified_frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release resources
    output_video.release()
    cv2.destroyAllWindows()
    stream.stop()
    # convert video from mp4v to h264
    subprocess.call(
        f"ffmpeg -i {temp_file} -i {temp_audio} -c:v libx264 -crf 20 -c:s copy -c:a aac -map 0:v:0 -map 1:a:0 {output_file}".split(
            " "
        )
    )
    # Get the path to the folder you want to delete all files from

    # Iterate over all the files in the folder
    for file_path in os.listdir("temp"):
        # Delete the file
        os.remove(os.path.join("temp", file_path))
    # subprocess.call(['ffmpeg','-y', '-i', temp_file, '-c:v', 'libx264', '-crf', '20', '-c:s', 'copy', '-c:a', 'copy', output_file])
    # decoder.terminate()
    return return_file


def get_curved_text(
    text, font, color, stroke_color, stroke_width, width, height, radius
):
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
        ch_d.text(
            (ch_image.size[0] / 2 - size[0] / 2, ch_image.size[1] / 2 - size[1] / 2),
            character,
            fill=color,
            font=font,
            stroke_fill=stroke_color,
            stroke_width=stroke_width,
            align="center",
        )
        ch_image = ch_image.rotate(
            math.degrees(angle), fillcolor="#00000000", resample=Image.BICUBIC
        )
        bg.paste(
            ch_image,
            (
                round(bg.size[0] / 2 + delta_x - ch_image.size[0] / 2),
                round(bg.size[1] / 2 + delta_y - ch_image.size[1] / 2),
            ),
            ch_image,
        )
    return bg
