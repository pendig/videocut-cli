# 🛠️ Development & Architecture Context

This document provides in-depth technical information regarding the architecture and workflow of VideoCut-CLI.

## 1. Layered Architecture
The project follows a modular pattern separating the interface (CLI), orchestration (Core), and specific functionality (Modules).

- **CLI Layer (`cli.py`)**: Uses `Typer` to handle command-line arguments and user interaction.
- **Orchestrator (`cli.py`)**: Currently orchestrates the `download`, `edit`, and `doctor` commands.
- **Modules (`/modules/`)**: 
  - `downloader.py`: Wrapper for `yt-dlp`. Uses a prioritized list of player clients (`android`, `web_embedded`, etc.) to bypass YouTube SABR 403 errors.
  - `editor.py`: Handles FFmpeg pipelines using `imageio-ffmpeg` as a fallback.

## 2. Output Data Structure
Files are stored in `{platform}/{video_id}/` relative to the download directory.
```text
~/Downloads/youtube/{video_id}/
├── {slug}_{id}_{res}.mp4 (Raw Video)
├── {slug}_{id}_{res}.jpg (Thumbnail)
├── {slug}_{id}_{res}.json (Raw yt-dlp metadata)
├── {slug}_{id}_{res}.vtt (Subtitles/Captions)
└── metadata_{id}.md (Cleaned Markdown Metadata)
```

## 3. Implementation Standards
- **FFmpeg**: Checks for system `ffmpeg` first, then falls back to `imageio-ffmpeg` binary.
- **Bypassing 403s**: Uses `android` player client in `yt-dlp` extractor arguments as it is currently the most stable for bypassing signature/SABR restrictions.
- **JS Runtime**: Requires `node` or `deno` for `yt-dlp` to handle YouTube's signature decryption.
- **Smart Skip**: Always verify if a file ID suffix exists before initiating a new download stream.

## 4. Presets (YAML)
Planned for `/presets/*.yaml`. The `reels` and `shorts` presets will define `aspect_ratio` and `caption_style`.

---
[Back to Index](./README.md)
