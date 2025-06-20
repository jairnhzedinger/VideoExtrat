from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.youtube_transcriber import download_video


class DummyStream:
    def __init__(self, tmpdir: Path):
        self.tmpdir = tmpdir

    def download(self, output_path: str, filename: str):
        path = Path(output_path) / filename
        path.write_text("data")
        return str(path)


class DummyStreams:
    def __init__(self, tmpdir: Path):
        self.tmpdir = tmpdir

    def filter(self, **kwargs):
        class Query:
            def __init__(self, stream):
                self._stream = stream

            def first(self):
                return self._stream

        return Query(DummyStream(self.tmpdir))


class DummyYouTube:
    def __init__(self, url: str, tmpdir: Path):
        self.url = url
        self._tmpdir = tmpdir

    @property
    def streams(self):
        return DummyStreams(self._tmpdir)

    @property
    def title(self):
        return "dummy"


def test_download_video_success(tmp_path):
    with patch("src.youtube_transcriber.YouTube", lambda url: DummyYouTube(url, tmp_path)):
        path = download_video("http://youtube.com/dummy", output_dir=str(tmp_path))
        assert path.exists()


def test_download_video_http_error(tmp_path):
    class FailYouTube:
        def __init__(self, url):
            raise HTTPError(url, 400, "Bad Request", None, None)

    with patch("src.youtube_transcriber.YouTube", FailYouTube):
        with pytest.raises(RuntimeError):
            download_video("http://bad.url", output_dir=str(tmp_path))
