# Motion_Extraction_For_Videos
A simple program that highlights any motion found in a video. Useful for stillshots with in-frame movement.

![ezgif com-video-to-gif-converter](https://github.com/Josh-Mak/Motion_Extraction_For_Videos/assets/152421096/e56f0dea-54ea-49ec-8613-a731f9955c2f)


**Intro**: I made this project as a way to learn more about video editing with code, and as a way to learn how to make a non web-based (eg. Flask) GUI. 

**Technical Overview**:
  1. Using CustomTKinter a GUI is made that allows the user to select which video to use and which settings to process it with.
  2. A combination of MoviePy and Pillow are used to process the video.
     - Two frames of the video are selected and compared, highlighting any differences.
     - The differences are saved as a mask and then colored green.
  3. The new green colored frames are compiled back into an mp4 using MoviePy.

**Future Improvements**: There are a couple of smaller improvements that could be readily added, such as GUI improvements like a loading bar, including a stabilization process in the app, and automatic optimal threshold detection, but the main improvement that would need to be made for a production level app is improving the algorithm to better detect motion and differences. As is, for a lot of video editing techniques that rely on masks like this, there is a lot of cleanup that has to be done after motion extraction.
