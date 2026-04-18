import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from pathlib import Path
import warnings
import os
import shutil

# Suppress all warnings to ensure clean CLI output
warnings.simplefilter("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["YT_DLP_NO_DEPRECATION_WARNING"] = "1"

from videocut.modules.downloader import download_video, check_ffmpeg, check_js_runtime
from videocut.modules.editor import add_text_watermark, add_image_watermark
from videocut.config import get_platform_dir, get_cookie_cache_path, get_cookie_store_path
import subprocess

app = typer.Typer(help="VideoCut CLI - Video and Download Automation Tool")
console = Console()

@app.command("download")
def download(
    url: str = typer.Argument(..., help="URL of the video to download"),
    quality: str = typer.Option("720", "-q", "--quality", help="Video quality (e.g., 360, 480, 720, 1080, best)"),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Custom output directory"),
    no_thumb: bool = typer.Option(False, "--no-thumb", help="Skip downloading thumbnail"),
    no_transcript: bool = typer.Option(False, "--no-transcript", help="Skip generating transcript"),
    metadata_only: bool = typer.Option(False, "--metadata-only", help="Only download metadata/thumbnail/transcript"),
    extract_audio: bool = typer.Option(False, "--extract-audio", help="Extract audio to MP3"),
    platform: Optional[str] = typer.Option(None, "--platform", help="Force platform name for directory (default: auto-detected)"),
    cookies_browser: Optional[str] = typer.Option(None, "--cookies-browser", help="Browser to extract cookies from"),
    cookies: Optional[Path] = typer.Option(None, "--cookies", help="Path to a Netscape cookies.txt file.")
):
    """Download video or audio from various platforms."""
    # Transform Shorts URL
    if "youtube.com/shorts/" in url:
        video_id = url.split("youtube.com/shorts/")[1].split("?")[0].split("&")[0]
        url = f"https://www.youtube.com/watch?v={video_id}"
        console.print(f"[dim]Converted Shorts URL to: {url}[/dim]")

    if platform is None:
        if "youtube.com" in url or "youtu.be" in url:
            platform = "youtube"
        else:
            platform = "instagram"
            
    target_dir = output if output else get_platform_dir(platform)
    stored_cookies = get_cookie_store_path()

    active_cookies = None
    if cookies:
        console.print(f"[dim]Saving provided cookies to {stored_cookies}[/dim]")
        shutil.copy(cookies, stored_cookies)
        active_cookies = stored_cookies
    elif cookies_browser:
        cache_path = get_cookie_cache_path(cookies_browser)
        if not cache_path.exists():
            console.print(f"[bold yellow]Extracting {cookies_browser} cookies...[/bold yellow]")
            try:
                subprocess.run([
                    "yt-dlp", "--cookies-from-browser", cookies_browser, 
                    "--cookies", str(cache_path), "--skip-download", "https://www.youtube.com"
                ], capture_output=True, check=True)
                shutil.copy(cache_path, stored_cookies)
            except Exception as e:
                console.print(f"[bold red]Failed to extract cookies: {e}[/bold red]")
        active_cookies = cache_path if cache_path.exists() else None
    
    # Try Download
    console.print(f"[bold cyan]Platform:[/bold cyan] [green]{platform}[/green]")
    
    # First attempt
    result_path = download_video(
        url=url, platform=platform, output_dir=target_dir, quality=quality,
        download_thumbnail=not no_thumb, download_transcript=not no_transcript,
        cookies_file=active_cookies, metadata_only=metadata_only, extract_audio=extract_audio
    )
    
    # Second attempt fallback
    if not result_path and not active_cookies and stored_cookies.exists():
        console.print("[yellow]Attempt failed. Retrying with stored cookies...[/yellow]")
        result_path = download_video(
            url=url, platform=platform, output_dir=target_dir, quality=quality,
            download_thumbnail=not no_thumb, download_transcript=not no_transcript,
            cookies_file=stored_cookies, metadata_only=metadata_only, extract_audio=extract_audio
        )
    
    if result_path:
        console.print(f"\n[bold green]✓ Successfully processed: {result_path}[/bold green]")
    else:
        console.print("\n[bold red]x Failed to process video bundle.[/bold red]")
        raise typer.Exit(code=1)

@app.command("edit")
def edit(
    video_path: Path = typer.Argument(..., help="Path to the video file to edit"),
    text: Optional[str] = typer.Option(None, "--text", help="Text to add as watermark"),
    image: Optional[Path] = typer.Option(None, "--image", help="Image to add as watermark"),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Path for the output video"),
    position: str = typer.Option("bottom_right", "--position", help="Position for the watermark")
):
    """Apply edits to a video (watermarking, etc.)."""
    if not video_path.exists():
        console.print(f"[bold red]File not found: {video_path}[/bold red]")
        raise typer.Exit(1)
    if output is None:
        output = video_path.parent / f"{video_path.stem}_edited.mp4"

    success = False
    if image:
        success = add_image_watermark(video_path, output, image, position)
    elif text:
        success = add_text_watermark(video_path, output, text, position)
    else:
        console.print("[yellow]No edit options provided. Use --text or --image.[/yellow]")
        return

    if success:
        console.print(f"[bold green]✓ Edit successful![/bold green] Saved to: {output}")
    else:
        console.print("[bold red]x Edit failed.[/bold red]")

@app.command("doctor")
def doctor():
    """Check system dependencies and environment health."""
    console.print("[bold cyan]🏥 VideoCut Doctor - System Health Check[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Dependency", style="dim")
    table.add_column("Status")
    table.add_column("Path/Details")

    # Check FFmpeg
    ffmpeg_path = check_ffmpeg()
    if ffmpeg_path:
        table.add_row("FFmpeg", "[green]✓ Found[/green]", ffmpeg_path)
    else:
        table.add_row("FFmpeg", "[red]x Missing[/red]", "Install via 'brew install ffmpeg'")

    # Check JS Runtime
    js_runtime = check_js_runtime()
    if js_runtime:
        table.add_row("JS Runtime", "[green]✓ Found[/green]", js_runtime)
    else:
        table.add_row("JS Runtime", "[yellow]! Missing[/yellow]", "Install 'node' or 'deno' for better YouTube support")

    # Check Python version
    py_version = f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    table.add_row("Python", "[green]✓ OK[/green]", py_version)

    # Check Cookie Store
    stored_cookies = get_cookie_store_path()
    cookie_status = "[green]✓ Exists[/green]" if stored_cookies.exists() else "[dim]Not setup[/dim]"
    table.add_row("Cookie Store", cookie_status, str(stored_cookies))

    console.print(table)
    
    if not ffmpeg_path:
        console.print("\n[bold red]Critical dependencies missing![/bold red] Please install FFmpeg to use VideoCut.")
    elif not js_runtime:
        console.print("\n[bold yellow]Note:[/bold yellow] YouTube downloads might be slower or unstable without a JS runtime (Node.js/Deno).")
    else:
        console.print("\n[bold green]System is healthy and ready to go![/bold green]")

if __name__ == "__main__":
    app()
