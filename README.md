# 🎬 VideoCut-CLI

**VideoCut-CLI** is an AI-powered command-line tool designed to help Content Creators automate their entire video workflow: from downloading and editing (trim, caption, watermark) to publishing on social media platforms.

---

## 🚀 Current Status (Phase 1: MVP)

- [x] **Smart Downloader**: 
  - High-quality video download (yt-dlp wrapper).
  - **SABR 403 Bypass**: Automatically uses Android player client.
  - **Cookie Persistence**: Saves and reuses cookies automatically.
  - **Smart Naming**: `{Title}_{ID}_{Resolution}.mp4` format.
  - **Smart Skip**: Skips already downloaded files.
  - **Modes**: Support for `--metadata-only` and `--extract-audio` (MP3).
- [x] **System Health**:
  - `videocut doctor` command to check FFmpeg and JS runtime status.
- [x] **Basic Editor**: 
  - Text and Image watermarking.
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

Install via **pipx** (recommended for CLI tools):

```bash
pipx install videocut-cli
```

Or via standard **pip**:

```bash
pip install videocut-cli
```

After installation, run the health check:
```bash
videocut doctor
```

---
*Created with ❤️ by [Pena Digital](https://penadigital.tech)*
