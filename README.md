# VideoExtrat

This project provides utilities to download videos from YouTube and transcribe
their audio using [Whisper](https://github.com/openai/whisper).

## Requirements

- Python 3.10
- [ffmpeg](https://ffmpeg.org/) available on the system path.
- Python packages listed in `requirements.txt`.

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To download a video and generate a transcript:

```bash
python -m src.youtube_transcriber <youtube-url>
```

The video and transcript will be placed in the `downloads/` directory.
