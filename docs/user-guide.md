# 🚀 Getting Started Guide

Want to start creating content with VideoCut-CLI? Follow these simple steps below!

## 1. Download Video
First, let's grab the video. Just copy the YouTube link and type this command:

```bash
videocut download https://youtube.com/your-link
```
*Result: The video will be saved to your computer, complete with its title and thumbnail.*

## 2. Edit to Your Likings
Once you have the video, you can edit it immediately for Reels or TikTok. For example, to add automatic captions and your account name as a watermark:

```bash
videocut edit <VIDEO_ID> --preset reels --caption --watermark "@MyAccount"
```
*Result: The video will be cropped to portrait size, captions will appear as people speak, and your account name will be in the corner.*

## 3. Use AI Powers
Want to make your video more advanced? Try these AI features:
- **Auto-Crop**: Let the AI find the most important part of the video and focus on it.
- **Dubbing**: Change the voice in the video to a cool AI voice in a different language.

```bash
videocut ai dub <VIDEO_ID> --target-lang en
```

## 4. Post Directly
No need to manually transfer files to your phone—just upload it!

```bash
videocut publish ./output-folder/video.mp4 --platform tiktok
```

---
💡 **Tip**: If you're unsure of what command to use next, you can always type `videocut --help` to see the help menu.
