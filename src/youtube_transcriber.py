"""Utility to download YouTube videos and transcribe them using Whisper."""

from pathlib import Path
from urllib.error import HTTPError
from pytube import YouTube


def download_video(url: str, output_dir: str = "downloads") -> Path:
    """Download the audio stream of a YouTube video.

    Parameters
    ----------
    url: str
        The YouTube video URL.
    output_dir: str, optional
        Directory where the video will be saved. Defaults to ``downloads``.

    Returns
    -------
    Path
        Path to the downloaded video file.
    """
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch video info: {exc}") from exc

    if stream is None:
        raise RuntimeError("No audio streams available for this video.")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_name = f"{yt.title.replace(' ', '_')}.mp4"
    try:
        stream.download(output_path=str(output_path), filename=file_name)
    except HTTPError as exc:
        raise RuntimeError(f"Failed to download video: {exc}") from exc
    except Exception as exc:  # catch other download errors
        raise RuntimeError(f"Failed to download video: {exc}") from exc
    return output_path / file_name


def transcribe_video(video_path: Path, model_size: str = "base") -> str:
    """Transcribe the given video using Whisper.

    Parameters
    ----------
    video_path: Path
        Path to the video file to transcribe.
    model_size: str, optional
        Size of the Whisper model to use. Defaults to ``base``.

    Returns
    -------
    str
        The transcribed text.
    """
    import whisper
    model = whisper.load_model(model_size)
    result = model.transcribe(str(video_path))
    return result.get("text", "")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Download a YouTube video and transcribe it.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--model", default="base", help="Whisper model size")
    parser.add_argument("--output-dir", default="downloads", help="Directory to store downloads")
    args = parser.parse_args()

    video = download_video(args.url, args.output_dir)
    print(f"Video saved to {video}")

    print("Starting transcription...")
    text = transcribe_video(video, args.model)
    transcript_file = Path(args.output_dir) / f"{video.stem}.txt"
    transcript_file.write_text(text, encoding="utf-8")
    print(f"Transcript saved to {transcript_file}")


if __name__ == "__main__":
    main()
