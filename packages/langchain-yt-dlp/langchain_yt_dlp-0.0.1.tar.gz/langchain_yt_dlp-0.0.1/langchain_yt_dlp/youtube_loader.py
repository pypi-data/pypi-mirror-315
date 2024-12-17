from typing import Dict, List, Union, Optional, Sequence, Any, Generator
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
from langchain_community.document_loaders.youtube import TranscriptFormat, _parse_video_id

class YoutubeLoader(BaseLoader):
    """Load YouTube video transcripts using yt-dlp."""
    def __init__(
        self,
        video_id: str,
        add_video_info: bool = False,
        language: Union[str, Sequence[str]] = 'en',
        translation: Optional[str] = None,
        transcript_format: TranscriptFormat = TranscriptFormat.TEXT,
        continue_on_failure: bool = False,
        chunk_size_seconds: int = 120,
    ):
        """Initialize with YouTube video ID."""
        self.video_id = video_id
        self._metadata = {"source": video_id}
        self.add_video_info = add_video_info
        self.language = language
        if isinstance(language, str):
            self.language = [language]
        self.translation = translation
        self.transcript_format = transcript_format
        self.continue_on_failure = continue_on_failure
        self.chunk_size_seconds = chunk_size_seconds

    @staticmethod
    def extract_video_id(youtube_url: str) -> str:
        """Extract video ID from common YouTube URLs."""
        video_id = _parse_video_id(youtube_url)
        if not video_id:
            raise ValueError(
                f'Could not determine the video ID for the URL "{youtube_url}".'
            )
        return video_id
    
    @classmethod
    def from_youtube_url(cls, youtube_url: str, **kwargs: Any) -> "YoutubeLoader":
        """Given a YouTube URL, construct a loader.
        See `YoutubeLoader()` constructor for a list of keyword arguments.
        """
        video_id = cls.extract_video_id(youtube_url)
        return cls(video_id, **kwargs)

    def load(self) -> List[Document]:
        """Load YouTube transcripts into 'Document' objects."""
        try:
            from youtube_transcript_api import (
                NoTranscriptFound,
                TranscriptsDisabled,
                YouTubeTranscriptApi
            )
        except ImportError:
            raise ImportError(
                'Could not import "youtube_transcript_api" Python package'
                "Please install it with 'pip install youtube-transcript-api'."
            )
        if self.add_video_info:
            video_info = self._get_video_info()
            self._metadata.update(video_info)
        
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        except TranscriptsDisabled:
            return []

        try:
            transcript = transcript_list.find_transcript(self.language)
        except NoTranscriptFound:
            transcript = transcript_list.find_transcript(["en"])
        
        if self.translation is not None:
            transcript = transcript.translate(self.translation)
        
        transcript_pieces: List[Dict[str, Any]] = transcript.fetch()

        if self.transcript_format == TranscriptFormat.TEXT:
            transcript = " ".join(
                map(
                    lambda transcript_piece: transcript_piece["text"].strip(" "),
                    transcript_pieces,
                )
            )
            return [Document(page_content=transcript, metadata=self._metadata)]
        elif self.transcript_format == TranscriptFormat.LINES:
            return list(
                map(
                    lambda transcript_piece: Document(
                        page_content=transcript_piece["text"].strip(" "),
                        metadata=dict(
                            filter(
                                lambda item: item[0] != "text", transcript_piece.item
                            )
                        ),
                    ),
                    transcript_pieces,
                )
            )
        elif self.transcript_format == TranscriptFormat.CHUNKS:
            return list(self._get_transcript_chunks(transcript_pieces))
        else:
            raise ValueError("Unknown transcript format.")
    
    def _get_video_info(self) -> Dict:
        """Get important video information.

        Components include:
            - title
            - description
            - thumbnail URL,
            - publish_date
            - channel author
            - and more.
        """
        try:
            from yt_dlp import YoutubeDL

        except ImportError:
            raise ImportError(
                'Could not import "yt_dlp" Python package. '
                "Please install it with `pip install yt_dlp`."
            )
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with YoutubeDL(ydl_opts) as ydl:
            yt = ydl.extract_info(
                f"https://www.youtube.com/watch?v={self.video_id}", download=False
            )
            publish_date = yt.get("upload_date")
            if publish_date:
                try:
                    from datetime import datetime

                    publish_date = datetime.strptime(publish_date, "%Y%m%d")
                except (ValueError, TypeError):
                    publish_date = "Unknown"
        video_info = {
            "title": yt.get("title", "Unknown"),
            "description": yt.get("description", "Unknown"),
            "view_count": yt.get("view_count", 0),
            "publish_date": publish_date,
            "length": yt.get("duration", 0),
            "author": yt.get("uploader", "Unknown"),
            "channel_id": yt.get("channel_id", "Unknown"),
            "webpage_url": yt.get("webpage_url", "Unknown"),
        }
        return video_info