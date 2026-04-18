# Data Workflow

This document explains how data flows through VideoCut-CLI and how output is organized.

## 1. Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant CLI
    participant Downloader
    participant Metadata
    participant Editor
    participant AI
    participant Publisher

    User->>CLI: videocut download <url>
    CLI->>Downloader: fetch(url, quality=720p)
    Downloader-->>FS: video.mp4 → Downloads/{platform}/{id}/
    
    CLI->>Metadata: extract(video_id)
    Metadata-->>FS: metadata_{id}.md, thumbnail.jpg, info.json
    
    opt --extract-audio flag active
        CLI->>Downloader: extract_audio(url)
        Downloader-->>FS: audio_{id}.mp3
    end

    opt --edit command active
        CLI->>Editor: apply_watermark(video)
        Editor-->>FS: video_edited.mp4
    end

    opt AI enhancement (Soon)
        CLI->>AI: process(video)
        AI-->>FS: output/
    end
```

## 2. Output Directory Structure

Files are organized by platform and video ID for easy management.

```text
~/Downloads/
└── {platform}/                     # e.g., youtube, instagram
    └── {video_id}/                 # e.g., ZDKJnLmEt0I
        ├── {slug}_{id}_{res}.mp4   # Original video (with resolution in name)
        ├── metadata_{id}.md        # Cleaned markdown metadata
        ├── {slug}_{id}_{res}.jpg   # Video thumbnail
        ├── {slug}_{id}_{res}.json  # Full raw yt-dlp metadata
        ├── {slug}_{id}_{res}.vtt   # Subtitles (if available)
        ├── {slug}_{id}_audio.mp3   # Audio extract (if requested)
        └── output/                 # (Soon) Result folder for editing/AI
```

## 3. Smart Skip Logic
VideoCut-CLI checks if the target files already exist in the `{video_id}` folder before starting a download. If found, it skips the redundant processing to save bandwidth and time.
