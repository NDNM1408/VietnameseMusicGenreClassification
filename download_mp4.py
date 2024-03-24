import os
import re
from pytube import YouTube
from pydub import AudioSegment

index = 0
category = "thieu_nhi" 
output_path = f"./audio/{category}"
links_file_path = f"./link_youtube/{category}.txt"

def download_audio_from_youtube(youtube_url):
    global index
    index += 1
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Filter for audio streams
        audio_streams = yt.streams.filter(only_audio=True)

        if audio_streams:
            # Get the highest quality audio stream
            audio_stream = audio_streams[0]

            yt.title = re.sub(r'[^\w\-_\. ]', '_', yt.title)

            file_name_mp3 = f"{index}_{yt.title}.mp3"
            file_name_wav = f"{index}_{yt.title}.wav"

            # Download the audio stream
            audio_stream.download(output_path, filename=file_name_mp3)

            print(f"{file_name_mp3} downloaded successfully.")

            # Convert mp3 to wav
            sound = AudioSegment.from_file(f"{output_path}/{file_name_mp3}")
            sound.export(f"{output_path}/{file_name_wav}", format="wav")
            print(f"{file_name_wav} converted successfully.")

            # Remove mp3 file
            os.remove(f"{output_path}/{file_name_mp3}")
        else:
            print("No audio streams found.")
    except Exception as e:
        print(f"Error: {str(e)}")


with open(links_file_path, "r") as file:
    youtube_urls = [line.strip() for line in file]

for youtube_url in youtube_urls:
    download_audio_from_youtube(youtube_url)
