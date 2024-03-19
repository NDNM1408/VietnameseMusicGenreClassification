from pytube import YouTube

def download_audio_from_youtube(youtube_url, output_path):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Filter for audio streams
        audio_streams = yt.streams.filter(only_audio=True)

        if audio_streams:
            # Get the highest quality audio stream
            audio_stream = audio_streams[0]

            # Download the audio stream
            audio_stream.download(output_path)

            print("Audio file downloaded successfully.")
        else:
            print("No audio streams found.")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
youtube_url = "https://www.youtube.com/watch?v=1mT_ALPymBg"  # Example YouTube URL
output_path = "./audio/"  # Output path where the audio file will be saved

download_audio_from_youtube(youtube_url, output_path)
