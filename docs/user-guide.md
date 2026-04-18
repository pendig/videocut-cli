# 🚀 Getting Started Guide

Want to start creating content with VideoCut-CLI? Follow these simple steps below!

## 1. Download Video
First, let's grab the video. Just copy the YouTube link and type this command:

```bash
# Standard download (Video + Metadata)
videocut download https://youtube.com/shorts/FwlIyiMeNAw

# Audio only (MP3)
videocut download https://youtube.com/shorts/FwlIyiMeNAw --extract-audio

# Metadata only (Small download, no video)
videocut download https://youtube.com/shorts/FwlIyiMeNAw --metadata-only
```
*Note: VideoCut-CLI automatically handles YouTube restrictions and remembers your cookies!*

## 2. Edit to Your Likings
Once you have the video, you can add watermarks easily:

```bash
videocut edit ./path/to/video.mp4 --text "@MyAccount" --position bottom_right
```

## 3. Use AI Powers (Coming Soon)
- **Auto-Crop**: Let the AI find the most important part of the video.
- **Dubbing**: Change the voice in the video to a cool AI voice.

---
💡 **Tip**: If you're unsure of what command to use next, you can always type `videocut --help` to see the help menu.
