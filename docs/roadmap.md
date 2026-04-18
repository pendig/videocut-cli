# Development Roadmap

This document outlines the current status and future plans for VideoCut-CLI.

## 🏁 Phase 1: MVP (Status: Nearly Complete)
Goal: A stable tool for daily download and basic editing.

- [x] **Smart Downloader**: 
  - `yt-dlp` wrapper with 403 bypass.
  - Automatic platform detection.
  - Dynamic naming `{Title}_{ID}_{Res}.mp4` and folder structure.
  - Support for `--extract-audio` and `--metadata-only` modes.
  - Cookie persistence system (`stored_cookies.txt`).
- [x] **Distribution**:
  - Official PyPI package: `videocut-cli`.
  - Official Homebrew Tap: `pendig/tap/videocut`.
- [x] **System Doctor**: 
  - Automated dependency checks for FFmpeg and JS runtime.
- [x] **Basic Editor**: 
  - Text and image watermarking functionality.
- [ ] **Auto-captioning**:
  - Integrate OpenAI Whisper for subtitle generation.
- [ ] **Preset System**:
  - Implement YAML-based configuration for Reels, Shorts, etc.

## 🤖 Phase 2: AI Core (Soon)
Goal: Intelligent video transformation for social media.

- [ ] **AI Auto-Crop**:
  - Intelligent 16:9 to 9:16 re-framing using YOLO or MediaPipe.
- [ ] **AI Highlights**:
  - Automatic detection of key moments based on transcript analysis.
- [ ] **AI Dubbing**:
  - Voice translation using ElevenLabs API.
- [ ] **AI Thumbnail**:
  - Smart thumbnail generation with text overlays.

## 🚀 Phase 3: Publisher & Integration (Soon)
Goal: One-click publishing to multiple platforms.

- [ ] **Direct Posting**:
  - Integration with YouTube Data API, TikTok API, and Instagram Graph API.
- [ ] **Scheduling**:
  - Queue videos for future publication.
- [ ] **IG/TikTok Downloader**:
  - Full support for Reels and TikTok link extraction.

## 💎 Phase 4: Final & Polish (Soon)
Goal: Collaborative features and advanced automation.

- [ ] **Plugin System**: Allow custom processors.
- [ ] **TUI Dashboard**: Interactive console interface using Rich.
- [ ] **n8n Integration**: Trigger workflows via webhooks.
