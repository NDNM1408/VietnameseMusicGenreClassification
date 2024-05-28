from utils import download_audio_from_youtube, extract_features

download_audio_from_youtube('https://www.youtube.com/watch?v=nM0xDI5R50E&list=RDTCuJXL_U_HA&index=3')
features = extract_features('data/audio.wav')
print(features)