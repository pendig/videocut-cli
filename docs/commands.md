# CLI Commands

Detailed reference for all VideoCut-CLI commands and options.

## 📥 `videocut download`
Downloads video or audio from supported platforms.

| Parameter | Type | Description |
|-----------|------|-------------|
| `URL` | Argument | Video URL (YouTube, IG, TikTok) |
| `-q, --quality` | Option | [360, 480, 720, 1080, best] (Default: 720) |
| `-o, --output` | Option | Custom output directory path |
| `--no-thumb` | Flag | Skip downloading thumbnail |
| `--no-transcript` | Flag | Skip generating transcript |
| `--metadata-only` | Flag | Only download metadata and thumbnail |
| `--extract-audio` | Flag | Download and convert to MP3 |
| `--cookies-browser` | Option | Browser to extract cookies from (e.g., chrome) |
| `--cookies` | Option | Path to a Netscape cookies.txt file |

### Examples:
```bash
videocut download https://youtu.be/dQw4w9WgXcQ
videocut download https://youtu.be/dQw4w9WgXcQ --extract-audio
```

---

## 🎬 `videocut edit`
Applies basic edits and watermarks to local video files.

| Parameter | Type | Description |
|-----------|------|-------------|
| `VIDEO_PATH` | Argument | Path to local file to edit |
| `--text` | Option | Text watermark |
| `--image` | Option | Image watermark path |
| `--position` | Option | Position: bottom_right, top_left, etc. |
| `-o, --output` | Option | Custom output path |
| `--preset` | Option | (Soon) base, reels, shorts |
| `--trim` | Option | (Soon) START:END format |

---

## 🏥 `videocut doctor`
Checks if your system is ready to use VideoCut-CLI.
- Verifies **FFmpeg** installation.
- Checks for **JS Runtime** (Node.js/Deno) for signature decryption.
- Displays current **Python** version.
- Shows **Cookie Store** status.

---

## 🤖 `videocut ai` (Soon)
- `ai crop`: AI-powered re-framing to 9:16 portrait.
- `ai highlights`: Automatically detect key moments.
- `ai dub`: Voice-over translation using ElevenLabs.
- `ai thumbnail`: Smart thumbnail generation.

---

## 🚀 `videocut publish` (Soon)
Directly upload processed videos to social media platforms.
- `--platform`: Target platform (youtube, ig, tiktok, x).
- `--schedule`: Set a publication time.

---

## ⚙️ `videocut config` (Soon)
Manage your API keys and global preferences.
- `--set KEY VALUE`: Store keys for ElevenLabs, YouTube API, etc.
- `--list`: View current configuration.

---

## 📦 `videocut batch` (Soon)
Process multiple URLs from a text file in parallel.
