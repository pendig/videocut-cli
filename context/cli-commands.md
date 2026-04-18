# ⌨️ CLI Command Schema

This document serves as a quick reference for all available CLI commands in VideoCut-CLI.

## 📥 `videocut download`
| Parameter | Type | Description |
|-----------|------|-------------|
| `URL` | Argument | Video URL (YouTube/IG/TikTok) |
| `-q, --quality` | Option | [360, 480, 720, 1080, best] |
| `-o, --output` | Option | Custom output directory |
| `--no-thumb` | Flag | Skip downloading thumbnail |
| `--no-transcript` | Flag | Skip generating transcript |
| `--metadata-only` | Flag | Only download metadata/thumbnail/transcript |
| `--extract-audio` | Flag | Extract audio to MP3 |
| `--cookies-browser` | Option | Browser to extract cookies from (e.g., chrome) |
| `--cookies` | Option | Path to a Netscape cookies.txt file |

## 🎬 `videocut edit`
| Parameter | Type | Description |
|-----------|------|-------------|
| `VIDEO_PATH` | Argument | Path to local file to edit |
| `--text` | Option | Text watermark |
| `--image` | Option | Image watermark path |
| `--position` | Option | Watermark position (bottom_right, etc.) |
| `-o, --output` | Option | Path for the output video |

## 🤖 `videocut ai` (Planned)
- `ai crop`: AI-powered re-framing to 9:16.
- `ai highlights`: Detect key moments in long-form videos.
- `ai dub`: Automatic dubbing using ElevenLabs API.
- `ai thumbnail`: Generate thumbnails with text overlays.

---
[Back to Index](./README.md)
