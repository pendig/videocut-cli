# 🎬 VideoCut-CLI

**VideoCut-CLI** is an AI-powered command-line tool designed to help Content Creators automate their entire video workflow: from downloading and editing (trim, caption, watermark) to publishing on social media platforms.

---

## 🚀 Current Status (Phase 1: MVP)

- [x] **Smart Downloader**: 
  - High-quality video download (yt-dlp wrapper).
  - **SABR 403 Bypass**: Automatically uses Android player client for stable YouTube downloads.
  - **Cookie Persistence**: Saves and reuses cookies from file or browser extracted cache.
  - **Smart Naming**: `{Title}_{ID}_{Resolution}.mp4` format.
  - **Smart Skip**: Skips already downloaded files to save time and bandwidth.
  - **Modes**: Support for `--metadata-only` and `--extract-audio` (MP3).
- [x] **Basic Editor**: 
  - Text and Image watermarking with position control.
- [ ] **AI Core (Planned)**: Auto-Crop (9:16), Highlights, Dubbing.

## 📁 Documentation Navigation

### 👨‍💻 [User Documentation](./docs/README.md)
*Path: `/docs`*
- Feature explanations and Quick start guide.

### 🤖 [AI Agent Context](./context/README.md)
*Path: `/context`*
- System architecture, schemas, and roadmap.

---

## 🛠️ Quick Installation

```bash
# Clone the repository
git clone https://github.com/penadigital/videocut-cli.git
cd videocut-cli

# Recommended: Use Python 3.9+ with venv
python -m venv venv
source venv/bin/activate
pip install -e .
```

---
*Created with ❤️ by [Pena Digital](https://penadigital.tech)*
