# https://github.com/db0htc/PyMotionExtraction/tree/main
import argparse
from moviepy.editor import VideoFileClip, ImageSequenceClip
from PIL import Image, ImageChops, ImageOps
import numpy as np
import os


# this returns an image from the current frame (new_image) with green pixels covering anything that is different from
# the previous frame. So anything that moved between frames is covered in green.
def combine_images(base_image, new_image, threshold, green_image):  # thresh default 50
    # Calculate the difference between the two images
    diff = ImageChops.difference(base_image, new_image)

    # Convert to grayscale and apply threshold to create a mask
    diff = diff.convert("L")
    mask = diff.point(lambda p: 255 if p > threshold else 0)  # if p (difference) is greater than threshhold, color it green. Else leave it the same.

    # Composite the green differences onto the new image using the threshold mask
    motion_image = Image.composite(green_image, new_image, mask)
    return motion_image


def process_video_target_motion(video_path, threshold=50, compare_first=False, by_interval=False, interval=1, first_to_last_only=False):
    clip = VideoFileClip(video_path)  # loads in the video under clip
    video_name = video_path.split("/")[1]
    # Create a green image to fill the mask the size of our video.
    green_image = Image.new("RGB", clip.size, color=(0, 255, 0))
    # green_image.save('green_image')
    clip_total_frames = clip.reader.nframes
    clip_fps = clip.fps
    duration = clip.duration
    current_time = 0.0
    first_frame = None
    previous_image = None
    frame_filenames = []

    if by_interval:
        while current_time <= duration:
            print(f"Processing time: {current_time}.")
            frame = clip.get_frame(current_time)
            image = Image.fromarray(frame)  # load frame as image

            if first_frame is None:
                first_frame = image  # setting the first frame variable

            if compare_first:  # default off
                motion_image = combine_images(first_frame, image, threshold, green_image)
            else:
                if previous_image is not None:
                    motion_image = combine_images(previous_image, image, threshold, green_image)
                else:
                    motion_image = combine_images(image, image, threshold, green_image)

            filename = f"frames_for_video/frame_time-{current_time}.png"
            motion_image.save(filename)
            frame_filenames.append(filename)

            previous_image = image
            current_time += interval

    elif first_to_last_only:
        first_frame = clip.get_frame(0)
        first_frame = Image.fromarray(first_frame)
        last_frame = clip.get_frame(duration - 0.1)
        last_frame = Image.fromarray(last_frame)

        motion_image = combine_images(first_frame, last_frame, threshold, green_image)
        motion_image.save(f'processed frames/first_vs_last_for_{video_name}-threshold_{threshold}.png')

    else:
        for i, frame in enumerate(clip.iter_frames()):  # for each frame in the video
            print(f"Processing frame #{i}/{clip_total_frames}.")
            image = Image.fromarray(frame)  # load frame as image

            if first_frame is None:
                first_frame = image  # setting the first frame variable

            if compare_first:  # default off
                motion_image = combine_images(first_frame, image, threshold, green_image)
            else:
                if previous_image is not None:
                    motion_image = combine_images(previous_image, image, threshold, green_image)
                else:
                    motion_image = combine_images(image, image, threshold, green_image)

            filename = f"frames_for_video/frame{i}.png"
            motion_image.save(filename)
            frame_filenames.append(filename)

            previous_image = image

    if by_interval:
        print(f"Finished all frames, creating video...")
        motion_video = ImageSequenceClip(frame_filenames, fps=1/interval)
        motion_video.write_videofile(f"processed videos/target_motion-{video_name}-threshold_{threshold}.mp4",
                                     fps=1/interval)
    else:
        if len(frame_filenames):
            print(f"Finished all frames, creating video...")
            motion_video = ImageSequenceClip(frame_filenames, clip_fps)
            motion_video.write_videofile(f"processed videos/target_motion-{video_name}-threshold_{threshold}.mp4", fps=clip_fps)

    print(f"Emptying stillframes folder.")
    for filename in os.listdir('frames_for_video'):
        if os.path.isfile(os.path.join('frames_for_video', filename)):
            os.remove(f"frames_for_video/{filename}")
