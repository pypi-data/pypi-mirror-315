# langchain-yt-dlp

**`langchain-yt-dlp`** is a Python package that extends [LangChain](https://github.com/langchain-ai/langchain) by providing an improved YouTube integration using `yt-dlp`. It allows users to fetch video metadata, transcripts, and other details from YouTube videos, with enhanced functionality compared to the original integration.

---

## Key Features

- Fetch YouTube transcripts with support for chunking, translations, and line-based formats.
- Retrieve additional video metadata (e.g., title, description, author, view count, publish date) using the `yt-dlp` library.
- Maintain compatibility with LangChain's existing loader interface.

---

## Installation

To install the package, use:

```bash
pip install langchain-yt-dlp
```

Ensure you have the following dependencies installed:
- `langchain`
- `yt-dlp`
- `youtube-transcript-api`

Install them with:
```bash
pip install langchain youtube-transcript-api yt-dlp
```

---

## Usage

Here’s how you can use the `YoutubeLoader` from `langchain-yt-dlp`:

### **Basic Example**



### **Loading From a YouTube URL**

```python
from langchain_yt_dlp.youtube_loader import YoutubeLoader

# Initialize using a YouTube URL
loader = YoutubeLoader.from_youtube_url(
    youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    add_video_info=True
)

documents = loader.load()
print(documents)
```

---

## Parameters

### `YoutubeLoader` Constructor

| Parameter            | Type                       | Default       | Description                                                                 |
|----------------------|----------------------------|---------------|-----------------------------------------------------------------------------|
| `video_id`           | `str`                     | None          | The YouTube video ID to fetch data for.                                    |
| `add_video_info`     | `bool`                    | `False`       | Whether to fetch additional metadata like title, author, etc.              |
| `language`           | `Union[str, Sequence[str]]`| `"en"`        | The language(s) for the transcript.                                        |
| `translation`        | `Optional[str]`           | `None`        | Language to translate the transcript into.                                 |
| `transcript_format`  | `TranscriptFormat`        | `"TEXT"`      | Format of the transcript (`TEXT`, `LINES`, or `CHUNKS`).                   |
| `chunk_size_seconds` | `int`                     | `120`         | Chunk size in seconds for splitting transcripts (if `CHUNKS` is used).     |
| `continue_on_failure`| `bool`                    | `False`       | Whether to continue loading even if an error occurs.                       |

---

## Testing

To run the tests:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/langchain-yt-dlp
   cd langchain-yt-dlp
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   pytest tests
   ```

---

## Contributing

Contributions are welcome! If you have ideas for new features or spot a bug, feel free to:
- Open an issue on [GitHub](https://github.com/yourusername/langchain-yt-dlp/issues).
- Submit a pull request.


---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for providing the base integration framework.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for enabling enhanced YouTube metadata extraction.
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript fetching.
