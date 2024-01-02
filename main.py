import tkinter
import customtkinter as ctk
import os
from target_motion import process_video_target_motion
from target_background import process_video_target_background

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("600x600")  # pixel height x width


def extract_motion():
    video_path = f"videos/{video_select_dropdown.get()}"
    threshold = round(threshold_slider_value.get(), 0)
    interval = round(interval_slider_value.get(), 2)

    if frame_to_compare.get() == "Compare to First Frame":
        compare_first = True
        first_to_last_only = False
    elif frame_to_compare.get() == "First to Last Frame":
        first_to_last_only = True
        compare_first = False
    else:
        compare_first = False
        first_to_last_only = False

    if comparison_frames.get() == "By Interval":
        by_interval = True
    else:
        by_interval = False
    print(f"Variables going into process function:")
    print(f"Video path: {video_path}")
    print(f"threshold: {threshold}")
    print(f"interval: {interval}")
    print(f"compare_first? {compare_first}")
    print(f"by_interval? {by_interval}")
    print(f"first_to_last_only? {first_to_last_only}")
    if selected_target.get() == "Target Background":
        process_video_target_background(video_path, threshold=threshold, compare_first=compare_first, by_interval=by_interval, interval=interval, first_to_last_only=first_to_last_only)
    elif selected_target.get() == "Target Motion":
        process_video_target_motion(video_path, threshold=threshold, compare_first=compare_first, by_interval=by_interval, interval=interval, first_to_last_only=first_to_last_only)


frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="Motion Extractor", font=("Roboto", 24))
title.place(relx=0.5, rely=0.05, anchor='center')

# region Video Selector
video_list = []
for filename in os.listdir('videos'):
    if os.path.isfile(os.path.join('videos', filename)):
        video_list.append(filename)
selected_video = tkinter.StringVar()
video_select_dropdown = ctk.CTkOptionMenu(master=frame, values=video_list, variable=selected_video)
video_select_dropdown.place(relx=0.5, rely=0.15, anchor='center')
# endregion

# region Selected Target Radios
selected_target = tkinter.StringVar()
target_motion_rad = ctk.CTkRadioButton(master=frame, text="Target Motion", variable=selected_target,
                                                 value="Target Motion")
target_motion_rad.place(relx=0.3, rely=0.25, anchor='w')
target_background_rad = ctk.CTkRadioButton(master=frame, text="Target Background", variable=selected_target,
                                                     value="Target Background")
target_background_rad.place(relx=0.55, rely=0.25, anchor='w')
# endregion

# region Compare to First vs Compare to last frame Radios
frame_to_compare = tkinter.StringVar()
compare_frame_to_first_rad = ctk.CTkRadioButton(master=frame, text="Compare to First Frame", variable=frame_to_compare,
                                                  value="Compare to First Frame")
compare_frame_to_first_rad.place(relx=0.03, rely=0.35, anchor='w')
compare_frame_to_previous_rad = ctk.CTkRadioButton(master=frame, text="Compare to Previous Frame", variable=frame_to_compare,
                                               value="Compare to Previous Frame")
compare_frame_to_previous_rad.place(relx=0.64, rely=0.35, anchor='w')
first_to_last_rad = ctk.CTkRadioButton(master=frame, text="First to Last Frame (img)", variable=frame_to_compare,
                                               value="First to Last Frame")
first_to_last_rad.place(relx=0.33, rely=0.35, anchor='w')
# endregion

# region Comparison Frames Radios
comparison_frames = tkinter.StringVar()
frame_by_frame_rad = ctk.CTkRadioButton(master=frame, text="Frame by Frame", variable=comparison_frames,
                                                  value="Frame by Frame")
frame_by_frame_rad.place(relx=0.3, rely=0.45, anchor='w')
by_interval_rad = ctk.CTkRadioButton(master=frame, text="By Interval (sec) - ", variable=comparison_frames,
                                               value="By Interval")
by_interval_rad.place(relx=0.55, rely=0.45, anchor='w')
# endregion


# region Interval Slider
def update_interval_slider_label(*args):
    interval_slider_label.configure(text=f"{round(interval_slider_value.get(), 2)}")


interval_slider_value = tkinter.DoubleVar()
interval_slider = ctk.CTkSlider(master=frame, width=130, height=16, from_=0, to=10, border_width=6,
                                variable=interval_slider_value)
interval_slider.place(relx=0.57, rely=0.5, anchor='w')
interval_slider_label = ctk.CTkLabel(master=frame, textvariable="")
interval_slider_label.place(relx=0.78, rely=0.45, anchor='w')
interval_slider_value.trace("w", update_interval_slider_label)
# endregion

# region Threshold Slider
threshold_label = ctk.CTkLabel(master=frame, text="Threshold", font=("Roboto", 18))
threshold_label.place(relx=0.5, rely=0.6, anchor='center')
threshold_i_label1 = ctk.CTkLabel(master=frame, text="Amount of difference needed to detect motion.", font=("Roboto", 12))
threshold_i_label1.place(relx=0.5, rely=0.65, anchor='center')
threshold_i_label2 = ctk.CTkLabel(master=frame, text="(Higher = Less motion detected. Lower = More motion detected.)", font=("Roboto", 12))
threshold_i_label2.place(relx=0.5, rely=0.685, anchor='center')


def update_threshold_slider_label(*args):
    threshold_slider_label.configure(text=f"{round(threshold_slider_value.get(), 0)}")


threshold_slider_value = tkinter.DoubleVar()
threshold_slider = ctk.CTkSlider(master=frame, width=220, height=20, from_=1, to=100, border_width=6,
                                variable=threshold_slider_value)
threshold_slider.place(relx=0.5, rely=0.8, anchor='center')
threshold_slider_label = ctk.CTkLabel(master=frame, textvariable="")
threshold_slider_label.place(relx=0.5, rely=0.75, anchor='center')
threshold_slider_value.trace("w", update_threshold_slider_label)
# endregion


extract_motion_btn = ctk.CTkButton(master=frame, text="Extract Motion", command=extract_motion)
extract_motion_btn.place(relx=0.5, rely=0.90, anchor='center')


root.mainloop()
