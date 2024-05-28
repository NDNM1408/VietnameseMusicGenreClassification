import librosa
import os
import re
from pytube import YouTube
from pydub import AudioSegment

def extract_vocal_segment(audio_file, duration=60, threshold=0.01):
    y, sr = librosa.load(audio_file, sr=22050)
    vocal_start_time = 30
    # Calculate start frame and end frame based on vocal_start_time and duration
    start_frame = int(librosa.time_to_samples(vocal_start_time, sr=sr))
    end_frame = start_frame + int(sr * duration)

    # Ensure the end frame is within the audio length
    if end_frame > len(y):
        end_frame = len(y)

    # Extract the vocal segment
    vocal_segment = y[start_frame:end_frame]

    return vocal_segment, sr

def extract_features(audio_path, num_mfcc=20, sample_rate=22050, n_fft=2048, chroma_hop_length=512):
    # Initialize the feature dictionary
    features = {
        "filename": os.path.basename(audio_path),
        "chroma_stft_mean": 0, "chroma_stft_var": 0,
        "rms_mean": 0, "rms_var": 0,
        "spectral_centroid_mean": 0, "spectral_centroid_var": 0,
        "spectral_bandwidth_mean": 0, "spectral_bandwidth_var": 0,
        "rolloff_mean": 0, "rolloff_var": 0,
        "zero_crossing_rate_mean": 0, "zero_crossing_rate_var": 0,
        "harmony_mean": 0, "harmony_var": 0,
        "perceptr_mean": 0, "perceptr_var": 0,
        "tempo": 0
    }

    for i in range(1, num_mfcc+1):
        features[f"mfcc{i}_mean"] = 0
        features[f"mfcc{i}_var"] = 0

    # Extract the vocal segment
    vocal_segment, sr = extract_vocal_segment(audio_path)

    # Chromagram
    chromagram = librosa.feature.chroma_stft(y=vocal_segment, sr=sr, hop_length=chroma_hop_length)
    features["chroma_stft_mean"] = chromagram.mean()
    features["chroma_stft_var"] = chromagram.var()
    
    # Root Mean Square Energy
    RMSEn = librosa.feature.rms(y=vocal_segment)
    features["rms_mean"] = RMSEn.mean()
    features["rms_var"] = RMSEn.var()
    
    # Spectral Centroid
    spec_cent = librosa.feature.spectral_centroid(y=vocal_segment)
    features["spectral_centroid_mean"] = spec_cent.mean()
    features["spectral_centroid_var"] = spec_cent.var()
    
    # Spectral Bandwidth
    spec_band = librosa.feature.spectral_bandwidth(y=vocal_segment, sr=sr)
    features["spectral_bandwidth_mean"] = spec_band.mean()
    features["spectral_bandwidth_var"] = spec_band.var()
    
    # Rolloff
    spec_roll = librosa.feature.spectral_rolloff(y=vocal_segment, sr=sr)
    features["rolloff_mean"] = spec_roll.mean()
    features["rolloff_var"] = spec_roll.var()
    
    # Zero Crossing Rate
    zero_crossing = librosa.feature.zero_crossing_rate(y=vocal_segment)
    features["zero_crossing_rate_mean"] = zero_crossing.mean()
    features["zero_crossing_rate_var"] = zero_crossing.var()
    
    # Harmonics and Percussive
    harmony, perceptr = librosa.effects.hpss(y=vocal_segment)
    features["harmony_mean"] = harmony.mean()
    features["harmony_var"] = harmony.var()
    features["perceptr_mean"] = perceptr.mean()
    features["perceptr_var"] = perceptr.var()
    
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=vocal_segment, sr=sr)
    features["tempo"] = float(tempo)
    
    # MFCCs
    mfcc = librosa.feature.mfcc(y=vocal_segment, sr=sr, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=chroma_hop_length)
    mfcc = mfcc.T
    for x in range(num_mfcc):
        features[f"mfcc{x+1}_mean"] = mfcc[:, x].mean()
        features[f"mfcc{x+1}_var"] = mfcc[:, x].var()
    
    return features

def download_audio_from_youtube(youtube_url):
    output_path = 'data'
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Filter for audio streams
        audio_streams = yt.streams.filter(only_audio=True)

        if audio_streams:
            # Get the highest quality audio stream
            audio_stream = audio_streams[0]

            yt.title = re.sub(r'[^\w\-_\. ]', '_', yt.title)

            file_name_mp3 = f"audio.mp3"
            file_name_wav = f"audio.wav"

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