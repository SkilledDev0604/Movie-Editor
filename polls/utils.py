from moviepy.editor import *
from django.conf import settings
from datetime import datetime
import math
from PIL import Image, ImageDraw, ImageFont
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
        return (10000, 10000)
    if i == 0:
        return (10000, 10000)
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
    width = abs(size[0] * math.cos(angle)) + abs(size[1] * math.sin(angle))
    height = abs(size[0] * math.sin(angle)) + abs(size[1] * math.cos(angle))
    # print(time, width, height, position_from, (
    #     position_from[0]
    #     + (position_to[0] - position_from[0]) * time
    #     - width * 0.5 * ((size_to - size_from) * time + size_from),
    #     position_from[1]
    #     + (position_to[1] - position_from[1]) * time
    #     - height * 0.5 * ((size_to - size_from) * time + size_from),
    # ))
    print(width, height)
    return (
        position_from[0]
        + (position_to[0] - position_from[0]) * time
        - width * 0.5,
        position_from[1]
        + (position_to[1] - position_from[1]) * time
        - height * 0.5,
    )



def get_text_size(text, font_file, fontsize):
    font = ImageFont.truetype(font_file, fontsize)
    return font.getsize(text)


def get_function_from_frames(frames, delta_x=0, delta_y=0, delta_r=0):
    x_func = ""
    y_func = ""
    f_func = ""
    r_func = ""
    previous_t = "0"
    previous_x = "0"
    previous_y = "0"
    previous_f = "1"
    previous_r = "0"
    for i, frame in enumerate(frames):
        t = frame["time"]
        x = frame["x"]
        y = frame["y"]
        f = frame["size"]
        r = frame["angle"]
        if i == 0:
            x_func += f"if(lte(t,{t}), W, "
            y_func += f"if(lte(t,{t}), H, "
            f_func += f"if(lte(t,{t}), 1, "
            r_func += f"if(lte(t,{r}), 0, "
        else:
            x_func += f"if(lte(t,{t}),  (t-{previous_t}) / (({t - previous_t})) * (({x}) - ({previous_x})) + ({previous_x}) - text_w/2, "
            y_func += f"if(lte(t,{t}),  (t-{previous_t}) / (({t - previous_t})) * (({y}) - ({previous_y})) + ({previous_y}) - text_h/2, "
            f_func += f"if(lte(t,{t}),  (t-{previous_t}) / (({t - previous_t})) * (({f}) - ({previous_f})) + ({previous_f}), "
            r_func += f"if(lte(t,{t}),  (t-{previous_t}) / (({t - previous_t})) * (({r}) - ({previous_r})) + ({previous_r}), "
        previous_t = t
        previous_x = x
        previous_y = y
        previous_f = f
        previous_r = r
    x_func += "W" + ")" * len(frames)
    y_func += "H" + ")" * len(frames)
    f_func += "1" + ")" * len(frames)
    r_func += "0" + ")" * len(frames)
    # x = delta_x * math.cos() - delta_y * math.sin(α)
    # y = delta_x * math.sin(α) + delta_y * math.cos(α)
    return (x_func, y_func, f_func, r_func)


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
    bg_clip = ColorClip(
        (round(max_width), round(max_height)), color=(0, 0, 0, 0), duration=duration
    )
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
    # print(size, scale)
    return scale


def make_video_1(form, image=None):
    videodir = f"{settings.BASE_DIR}\\static\\videos\\PawPatrolVideoInvitaion\\"
    input_file = videodir + "basic.mp4"
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    output_file = f"{videodir}output_{now}.mp4"
    image_file = image
    font_file = f"{settings.BASE_DIR}\\static\\fonts\\Aachen BT Bold font.ttf"

    # Open video stream
    stream = CamGear(source=input_file).start()

    # Define the text properties
    text = "Hello, World!"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 5
    font_color = (255, 255, 255)  # white color
    thickness = 6  # thickness of the text

    # Define output video writer
    output_path = output_file
    output_fps = stream.framerate
    output_height, output_width = stream.frame.shape[:2]
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
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
            "stroke_color": "gray",
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


    count = 0
    while True:
        
        # Read frames from the video stream
        frame = stream.read()

        # Break the loop if the video has ended
        if frame is None:
            break
        time = count / stream.framerate
        count += 1
        # Create a blank canvas with the same size as the frame
        pil_frame = Image.fromarray(frame)
        # Create a drawing object
        draw = ImageDraw.Draw(pil_frame)

        for text_object in text_objects:


            # Specify the text content and position
            text = text_object['text']
            # Load the custom font
            font = ImageFont.truetype(text_object['font_file'], size=round(text_object['fontsize'] * get_scale(time, text_object['frames'])))
            size = draw.textsize(text, font)
            print((width, height), size)
            text_position = get_position(t=time, frames=text_object['frames'], size=size)
            
            # Draw the text on the image
            draw.text(text_position, text, fill=text_object['color'], font=font, stroke_fill=text_object['stroke_color'], stroke_width=text_object['stroke_width'], align='center')

        # Convert the modified PIL Image back to OpenCV format
        modified_frame = np.array(pil_frame)

        output_video.write(modified_frame)

        # Display the output frame
        # cv2.imshow("Output", modified_frame)
        # Calculate the current frame's timestamp
        

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    output_video.release()
    cv2.destroyAllWindows()
    stream.stop()
    return output_file
    ffmpeg_input = ffmpeg.input(input_file)
    ffmpeg_output = ffmpeg_input
    
    
    # y = "0.25 * H"
    # text_objects.append({
    #         "text" : f"{form['linea3']}",
    #         "fontsize" : 70,
    #         "font_file" : font_file,
    #         "color" : 'white',
    #         "stroke_width" : 5,
    #         "stroke_color" : "gray",
    #         "frames": (
    #             {"time": 0, "x": x, 'y':y, "size": 0.1 * 70, "angle": 0},
    #             {"time": 0.1, "x":x, "y":y, "size": 1.2 * 70, "angle": 0},
    #             {"time": 0.2, "x":x, "y":y, "size": 1 * 70, "angle": 0},
    #             {"time": 3.8, "x":x, "y":y, "size": 1 * 70, "angle": 0},
    #             {"time": 3.9, "x":x, "y":y, "size": 1.2 * 70, "angle": 0, },
    #             {"time": 4, "x":x, "y":y, "size": 0.1 * 70, "angle": 0}
    #         ),
    #         "radius": 0
    #     })
    try:
        if image_file:
            ffmpeg_output = ffmpeg_input.overlay(
                ffmpeg.input(image_file), x="W-w-10", y="H-h-10"
            )
        for text_object in text_objects:
            if text_object["radius"] == 0:
                x_func, y_func, f_func, r_func = get_function_from_frames(text_object['frames'])
                ffmpeg_output = ffmpeg_output.drawtext(
                    text=text_object["text"],
                    x=x_func,
                    y=y_func,
                    fontsize=f_func,
                    fontcolor=text_object["color"],
                    fontfile=text_object["font_file"],
                    bordercolor=text_object["stroke_color"],
                    borderw=text_object["stroke_width"],
                    rotate=r_func,
                ).rotate(45)
            else:
                text_clips = []
                width = get_text_size(text_object["text"])
                sum_width = 0
                radius = text_object["rotate"]
                for c in text_object["text"]:
                    length = width / 2 - sum_width - get_text_size(c)[0] / 2
                    sum_width += get_text_size(c)[0]
                    angle = length / radius
                    delta_x = -radius * math.sin(angle)
                    delta_y = radius - radius * math.cos(angle)
                    x_func, y_func, f_func, r_func = get_function_from_frames(
                        text_object["frames"],
                        delta_x=delta_x,
                        delta_y=delta_y,
                        delta_r=angle,
                    )
                    ffmpeg_output = ffmpeg_output.drawtext(
                        text=text_object["text"],
                        x=x_func,
                        y=y_func,
                        fontsize=f_func,
                        fontcolor=text_object["color"],
                        fontfile=text_object["font_file"],
                        bordercolor=text_object["stroke_color"],
                        borderw=text_object["stroke_width"],
                        rotate=r_func,
                    )

            ffmpeg.output(ffmpeg_output, output_file).run()
    except ffmpeg.Error as e:
        print("ffmpeg error:", e.stderr.decode(), file=sys.stderr)

    return output_file
    # Load the video file
    video_file = VideoFileClip()
    ratio = 1.5
    video_file = video_file.resize([video_file.w * ratio, video_file.h * ratio])
    clips = [video_file]

    # Get the width and height of the video
    width, height = video_file.size

    # if image:
    #     image_clip = ImageClip(image)
    #     height_ratio = 0.3 * H / image_clip.h
    #     width_ratio = width / image_clip.w
    #     if height_ratio < width_ratio:
    #         image_clip = image_clip.resize(
    #             (image_clip.w * height_ratio, image_clip.h * height_ratio)
    #         )
    #     else:
    #         image_clip = image_clip.resize(
    #             (image_clip.w * W"_ratio, image_clip.h * W"_ratio)
    #         )
    #     y = 0.2 * H
    #     delta_x = 20
    #     frames = (
    #         {
    #             "time": 4,
    #             "x":0.5 * W" - delta_x, "y":y,
    #             "size": 1,
    #             "angle": 0,
    #             "opacity": 0,
    #         },
    #         {
    #             "time": 4.5,
    #             "x":0.5 * W" - delta_x, "y":y,
    #             "size": 1,
    #             "angle": 0,
    #         },
    #         {"time": 10, "x":0.5 * W" + delta_x, "y":y, "size": 1, "angle": 0},
    #     )
    #     image_clip = set_frames(image_clip, frames)
    #     clips.append(image_clip)
    #     x = 0.75 * W"
    #     y = 0.5 * H
    #     frames = (
    #         {"time": 11.5, "x":0.5 * W", "y":y, "size": 0.5, "angle": 0},
    #         {"time": 11.6, "x":x, "y":y, "size": 1.2, "angle": 0},
    #         {"time": 11.7, "x":x, "y":y, "size": 1, "angle": 0},
    #         {"time": video_file.duration, "x":x, "y":y, "size": 1, "angle": 0},
    #     )
    #     image_clip = set_frames(image_clip, frames)
    #     clips.append(image_clip)

    # BEN
    text_clip = get_curved_text_clip(
        f"{form['linea4']}",
        font="Arial-Bold",
        fontsize=150 * ratio,
        color="#251E87",
        stroke_color="white",
        stroke_width=8,
        max_width=video_file.w * 2,
        max_height=video_file.h * 2,
        radius=400,
    )
    clip_width, clip_height = text_clip.size
    delta_x = "-10"
    y = "0.45 * H"
    frames = (
        {"time": 5, "x": "W / 2" + delta_x, "y": y + " + 200", "size": 1, "angle": 0},
        {"time": 5.25, "x": "W / 2" + delta_x, "y": y, "size": 1, "angle": 0},
        {"time": 10.75, "x": "W / 2" + delta_x, "y": y, "size": 1, "angle": 0},
        {"time": 11, "x": "W / 2" + delta_x, "y": y + "-200", "size": 1, "angle": 0},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # IS TUNING
    text_clip = get_curved_text_clip(
        f"{form['linea5']}",
        font="Arial-Bold",
        fontsize=35 * ratio,
        color="#251E87",
        radius=400,
        max_height=video_file.h,
        max_width=video_file.w,
    )
    clip_width, clip_height = text_clip.size
    delta_x = -10
    y = 0.55 * H
    frames = (
        {"time": 5.5, "x": f"0.5 * W {delta_x}", "y": y, "size": 0.1, "angle": 0},
        {"time": 5.6, "x": "0.5 * W{delta_x}", "y": y, "size": 1.2, "angle": 0},
        {"time": 5.7, "x": "0.5 * W{delta_x}", "y": y, "size": 1, "angle": 0},
        {"time": 10.8, "x": "0.5 * W{delta_x}", "y": y, "size": 1, "angle": 0},
        {"time": 10.9, "x": "0.5 * W{delta_x}", "y": y, "size": 1.2, "angle": 0},
        {"time": 11, "x": "0.5 * W{delta_x}", "y": y, "size": 0.1, "angle": 0},
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # 2
    text_clip = TextClip(
        f"{form['linea6']}",
        font="Arial-Bold",
        fontsize=250 * ratio,
        color="#0CC0DF",
        stroke_color="white",
        stroke_width=10,
    )
    clip_width, clip_height = text_clip.size
    delta_x = -10
    y = "0.75 * H"
    frames = (
        {"time": 6, "x": "W", "y": y, "size": 0.1, "angle": -30},
        {"time": 6.2, "x": "0.5 * W", "y": y, "size": 1, "angle": 0},
        {"time": 10.8, "x": "0.5 * W", "y": y, "size": 1, "angle": -70},
        {"time": 11, "x": "0.5 * W", "y": "H", "size": 1, "angle": -45},
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
        fontsize=50 * ratio,
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
    y = "0.08 * H"
    frames = (
        {"time": 11.5, "x": "0.5 * W", "y": y, "size": 0.1, "angle": 0},
        {"time": 11.6, "x": "0.5 * W", "y": y, "size": 1.2, "angle": 0},
        {"time": 11.7, "x": "0.5 * W", "y": y, "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "x": "0.5 * W",
            "y": y,
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
        fontsize=40 * ratio,
        color="#251E87",
        stroke_color="white",
        stroke_width=2,
    )
    text_clip2 = TextClip(
        f"{form['linea11']}",
        font="Arial-Bold",
        fontsize=40 * ratio,
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
    y = 0.225 * H
    frames = (
        {"time": 12, "x": "0.5 * W", "y": y, "size": 0.1, "angle": 0},
        {"time": 12.1, "x": "0.5 * W", "y": y, "size": 1.2, "angle": 0},
        {"time": 12.2, "x": "0.5 * W", "y": y, "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "x": "0.5 * W",
            "y": y,
            "size": 1,
            "angle": 0,
        },
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    text_clip = TextClip(
        f"{form['linea12']}\n{form['linea13']}",
        font="Arial-Bold",
        fontsize=25 * ratio,
        color="black",
    )
    y = 0.325 * H
    frames = (
        {"time": 12.5, "x": "0.5 * W", "y": y, "size": 0.1, "angle": 0},
        {"time": 12.6, "x": "0.5 * W", "y": y, "size": 1.2, "angle": 0},
        {"time": 12.7, "x": "0.5 * W", "y": y, "size": 1, "angle": 0},
        {
            "time": video_file.duration - 0.1,
            "x": "0.5 * W",
            "y": y,
            "size": 1,
            "angle": 0,
        },
        s,
    )
    text_clip = set_frames(text_clip, frames)
    clips.append(text_clip)

    # Overlay the text clip on the video
    final_clip = CompositeVideoClip(clips)

    # Write the final video file
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    final_clip.write_videofile(f"{videodir}output_{now}.mp4")

    return f"videos/PawPatrolVideoInvitaion/output_{now}.mp4"
