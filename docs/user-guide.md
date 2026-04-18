# 🚀 Getting Started Guide

Follow these steps to start automating your video content creation.

## 0. Installation
The recommended way to install VideoCut-CLI is via **pipx** to ensure an isolated environment.

```bash
pipx install videocut-cli
```

### Health Check
After installation, run the doctor command to verify system dependencies (like FFmpeg).
```bash
videocut doctor
```

## 1. Downloading Content
VideoCut-CLI automatically handles restrictions and organizes your files.

```bash
# Full download (Video + Metadata)
videocut download "https://youtube.com/shorts/FwlIyiMeNAw"

# Audio only (MP3)
videocut download "URL" --extract-audio

# Metadata only (No video, fast research)
videocut download "URL" --metadata-only
```

## 2. Basic Editing
Add your brand identity to any local video file.

```bash
# Add a text watermark
videocut edit ./video.mp4 --text "@MyAccount" --position bottom_right

# Add an image logo
videocut edit ./video.mp4 --image ./logo.png
```

## 3. Advanced Features (Soon)
- **AI Auto-Crop**: Transform 16:9 videos to 9:16 portrait.
- **Voice Dubbing**: Translate your video audio using AI.
- **Batch Processing**: Download and edit hundreds of links at once.

---
💡 **Tip**: Type `videocut --help` or `videocut download --help` for a full list of options.
