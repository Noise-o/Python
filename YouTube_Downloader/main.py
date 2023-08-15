import moviepy.editor
from tkinter.filedialog import *
import pytube


# Tkinter
video = askopenfilename()

# MoviePy
video = moviepy.editor.VideoFileClip(video)
audio = video.audio
audio.write_audiofile('sample.mp3')


# # Pytube
# url =  'https://www.youtube.com/watch?v=qZt8qVK7KlQ'
# video = pytube.YouTube(url)
# video.streams.get_highest_resolution().download()