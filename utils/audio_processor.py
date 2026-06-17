from pytubefix import YouTube
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)



def download_youtube(url: str, out_dir: str = DOWNLOAD_DIR) -> str:
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
    stream = yt.streams.filter(only_audio=True).first()
    mp4_path = stream.download(output_path=out_dir, filename="audio.mp4")
    wav_path = convert_to_wav(mp4_path)
    return wav_path



def convert_to_wav(input_path : str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str, chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    
    chunks = []
    
    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i+1}.wav"
        chunk.export(chunk_path, format="wav")
        
        chunks.append(chunk_path)
        
    return chunks



def process_input(source : str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube URL. Downloading audio ...")
        wav_path = download_youtube(source)
    else:
        print("Detected local file. Converting to WAV ...")
        wav_path = convert_to_wav(source)
    print("Chunking audio ...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks