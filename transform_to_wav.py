from os import path
from pydub import AudioSegment

# files
src = "audio/1.mp4"
dst = "wav/1.wav"

# convert mp4 to wav
sound = AudioSegment.from_file(src,format="mp4")
sound.export(dst, format="wav")