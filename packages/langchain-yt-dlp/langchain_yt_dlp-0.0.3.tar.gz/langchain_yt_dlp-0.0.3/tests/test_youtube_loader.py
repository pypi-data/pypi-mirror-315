import pytest
from unittest.mock import patch
from langchain_yt_dlp.youtube_loader import YoutubeLoader

# Mock YouTube video ID for testing
TEST_VIDEO_ID = "dQw4w9WgXcQ"

def test_extract_video_id():
    """Test extracting video ID from a YouTube URL."""
    youtube_url = f"https://www.youtube.com/watch?v={TEST_VIDEO_ID}"
    extracted_id = YoutubeLoader.extract_video_id(youtube_url)
    assert extracted_id == TEST_VIDEO_ID

def test_init_with_video_id():
    """Test initializing YoutubeLoader with video ID."""
    loader = YoutubeLoader(video_id=TEST_VIDEO_ID, add_video_info=False)
    assert loader.video_id == TEST_VIDEO_ID
    assert not loader.add_video_info
    assert loader._metadata["source"] == TEST_VIDEO_ID

def test_init_with_video_info():
    """Test initializing YoutubeLoader with video info enabled."""
    loader = YoutubeLoader(video_id=TEST_VIDEO_ID, add_video_info=True)
    assert loader.add_video_info

@patch("langchain_yt_dlp.youtube_loader.YoutubeLoader._get_video_info")
def test_load_with_video_info(mock_get_video_info):
    """Test load() when add_video_info is True."""
    mock_get_video_info.return_value = {"title": "Test Video", "author": "Test Channel"}
    loader = YoutubeLoader(video_id=TEST_VIDEO_ID, add_video_info=True)
    loader.load()  # Will call _get_video_info()
    assert loader._metadata["title"] == "Test Video"
    assert loader._metadata["author"] == "Test Channel"

@patch("langchain_yt_dlp.youtube_loader.YoutubeLoader._get_video_info")
def test_get_video_info(mock_get_video_info):
    """Test the metadata extraction using _get_video_info."""
    mock_get_video_info.return_value = {
        "title": "Test Video",
        "author": "Test Channel",
        "view_count": 123456,
        "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }
    loader = YoutubeLoader(video_id=TEST_VIDEO_ID, add_video_info=True)
    video_info = loader._get_video_info()
    assert video_info["title"] == "Test Video"
    assert video_info["view_count"] == 123456
    assert video_info["author"] == "Test Channel"
    assert video_info["webpage_url"] == f"https://www.youtube.com/watch?v={TEST_VIDEO_ID}"
