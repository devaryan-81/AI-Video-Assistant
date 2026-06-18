from pydub import AudioSegment
import os
import tempfile

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def save_uploaded_file(uploaded_file) -> str:
    """Save a Streamlit UploadedFile to disk and return the path."""
    suffix = os.path.splitext(uploaded_file.name)[-1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=DOWNLOAD_DIR)
    tmp.write(uploaded_file.read())
    tmp.flush()
    tmp.close()
    return tmp.name


def download_youtube_audio(url: str) -> str:
    """Download YouTube audio locally using yt-dlp (local dev only)."""
    import yt_dlp

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    # Use local Windows ffmpeg if present, otherwise let yt-dlp find it in PATH
    ffmpeg_local = r"E:/ffmpeg-8.1.1-essentials_build/ffmpeg-8.1.1-essentials_build/bin"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
    }
    if os.path.isdir(ffmpeg_local):
        ydl_opts["ffmpeg_location"] = ffmpeg_local

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        filename = filename.replace(".webm", ".wav").replace(".m4a", ".wav")

    return filename


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i+1}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source) -> list:
    """
    Accepts:
      - Streamlit UploadedFile object  → save to disk, convert, chunk
      - A URL string (http/https)      → download via yt-dlp (local dev only)
      - A local file path string       → convert, chunk
    """
    if hasattr(source, "read"):
        # Streamlit UploadedFile — works on Streamlit Cloud
        print("Received uploaded file. Saving to disk ...")
        raw_path = save_uploaded_file(source)
        print("Converting to WAV ...")
        wav_path = convert_to_wav(raw_path)

    elif isinstance(source, str) and (source.startswith("http://") or source.startswith("https://")):
        # YouTube URL — local dev only (blocked on Streamlit Cloud)
        print("Detected YouTube URL. Downloading audio ...")
        wav_path = download_youtube_audio(source)

    elif isinstance(source, str):
        # Local file path
        print("Detected local file. Converting to WAV ...")
        wav_path = convert_to_wav(source)

    else:
        raise ValueError(f"Unsupported source type: {type(source)}")

    print("Chunking audio ...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks