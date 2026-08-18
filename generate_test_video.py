from gtts import gTTS
import os
import imageio_ffmpeg

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
tts = gTTS("The famous equation E = mc² describes energy.", lang='en')
tts.save("/mnt/d/SIH/test_audio.mp3")

# Generate video
os.system(f'{ffmpeg_path} -i /mnt/d/SIH/test_audio.mp3 -f lavfi -i color=c=black:s=128x128 -c:v libx264 -shortest -c:a aac /mnt/d/SIH/test_video.mp4 -y')
print("Video generated successfully.")
