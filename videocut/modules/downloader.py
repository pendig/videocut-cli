import os
import json
import shutil
from pathlib import Path
import yt_dlp
from rich.console import Console
from typing import Optional
import imageio_ffmpeg

console = Console()

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def check_ffmpeg():
    """Checks if ffmpeg is installed and returns the path."""
    # First check system path
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    
    # Fallback to imageio-ffmpeg bundled binary
    try:
        bundled_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled_ffmpeg:
            return bundled_ffmpeg
    except Exception:
        pass
    
    return None

def check_js_runtime():
    """Checks if a JS runtime (Node/Deno) is available for yt-dlp signatures."""
    return shutil.which("node") or shutil.which("deno")

def download_video(
    url: str,
    platform: str,
    output_dir: Path,
    quality: str = "720",
    download_thumbnail: bool = True,
    download_transcript: bool = True,
    cookies_browser: Optional[str] = None,
    cookies_file: Optional[Path] = None
) -> Optional[Path]:
    """
    Downloads a video from the specified URL using yt-dlp.
    Stores files in {output_dir}/<video_id>/.
    """
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        console.print("[bold red]Error: FFmpeg not found! Please install it via Homebrew or ensure imageio-ffmpeg is installed.[/bold red]")
        return None
        
    js_runtime = check_js_runtime()
    if not js_runtime:
        console.print("[bold yellow]Warning: No JS runtime (Node.js/Deno) found.[/bold yellow]")
        console.print("[dim]YouTube 403 errors are common without a JS runtime. Consider 'brew install deno'.[/dim]")
    else:
        console.print(f"[dim]JS Runtime Found: {js_runtime}[/dim]")
    
    # We first extract info without downloading to get the video id
    ydl_opts_extract = {
        'extract_flat': 'in_playlist',
        'quiet': True,
    }
    
    if cookies_browser:
        ydl_opts_extract['cookiesfrombrowser'] = (cookies_browser, None, None, None)
    elif cookies_file:
        ydl_opts_extract['cookiefile'] = str(cookies_file)
    
    with yt_dlp.YoutubeDL(ydl_opts_extract) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id', 'unknown_id')
            title = info.get('title', 'Unknown Title')
            console.print(f"[bold cyan]Video Found:[/bold cyan] {title}")
        except Exception as e:
            # Silence internal errors, just show a clean message
            return None

    # Target directory for this specific video
    video_dir = output_dir / video_id
    os.makedirs(video_dir, exist_ok=True)
    
    # Map quality to format string
    # Force legacy formats (18=360p, 22=720p) first as they often bypass SABR 403 errors
    format_str = f'18/22/bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
    if quality == "best":
        format_str = '22/18/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
    ydl_opts = {
        'format': format_str,
        'outtmpl': str(video_dir / f'video_{quality}p.%(ext)s'),
        'writethumbnail': download_thumbnail,
        'writesubtitles': download_transcript,
        'writeautomaticsub': download_transcript,
        'subtitleslangs': ['en', 'id'],
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
            {
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
            }
        ],
        # Save metadata to json
        'writeinfojson': True,
        # Default stability flags
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_color': True,
        'no_warnings': True,
        'logger': SilentLogger(),
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web_embedded', 'ios', 'tv', 'web'],
                'formats': 'missing_pot',
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        },
        'ffmpeg_location': ffmpeg_path,
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'retries': 5,
        'socket_timeout': 30,
    }
    
    if cookies_browser:
        ydl_opts['cookiesfrombrowser'] = (cookies_browser, None, None, None)
    elif cookies_file:
        ydl_opts['cookiefile'] = str(cookies_file)

    console.print(f"[bold blue]Downloading...[/bold blue] [dim](this may take a moment)[/dim]")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            
            # Verify if the video file actually exists (not just thumbnail)
            # Find any file starting with 'video_' and not ending in .webp, .jpg, .json, .md
            video_files = [f for f in video_dir.iterdir() if f.name.startswith("video_") and f.suffix not in ['.webp', '.jpg', '.json', '.md', '.vtt']]
            
            if not video_files:
                return None

            console.print("[bold green]✓ Download complete![/bold green]")
            
            # Post-process: convert info.json to a cleaner metadata.md
            info_json_path = list(video_dir.glob("*.info.json"))
            if info_json_path:
                create_metadata_md(info_json_path[0], video_dir / "metadata.md")
                
            return video_dir
        except Exception:
            return None

def create_metadata_md(json_path: Path, md_path: Path):
    """Converts yt-dlp info.json to a clean md file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        title = data.get('title', 'Unknown')
        uploader = data.get('uploader', 'Unknown')
        description = data.get('description', 'No description')
        tags = data.get('tags', [])
        
        md_content = f"# {title}\n\n"
        md_content += f"**Uploader**: {uploader}\n\n"
        md_content += f"## Description\n{description}\n\n"
        md_content += f"## Tags\n{', '.join(tags) if isinstance(tags, list) else ''}\n"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    except Exception as e:
        console.print(f"[yellow]Failed to generate metadata.md: {e}[/yellow]")
