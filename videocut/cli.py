import typer
from rich.console import Console
from typing import Optional
from pathlib import Path
import warnings
import os

# Suppress all warnings to ensure clean CLI output
warnings.simplefilter("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

from videocut.modules.downloader import download_video
from videocut.modules.editor import add_text_watermark, add_image_watermark
from videocut.config import get_platform_dir, get_cookie_cache_path
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
    platform: Optional[str] = typer.Option(None, "--platform", help="Force platform name for directory (default: auto-detected)"),
    cookies_browser: Optional[str] = typer.Option(None, "--cookies-browser", help="Browser to extract cookies from"),
    cookies: Optional[Path] = typer.Option(None, "--cookies", help="Path to a Netscape cookies.txt file. Recommended: Use 'Get cookies.txt LOCALLY' Chrome extension.")
):
    # Transform Shorts URL to standard Video URL (helpful for some SABR issues)
    if "youtube.com/shorts/" in url:
        video_id = url.split("youtube.com/shorts/")[1].split("?")[0].split("&")[0]
        url = f"https://www.youtube.com/watch?v={video_id}"
        console.print(f"[dim]Converted Shorts URL to: {url}[/dim]")

    # Auto-detect platform from URL if not specified
    if platform is None:
        if "youtube.com" in url or "youtu.be" in url:
            platform = "youtube"
        elif "instagram.com" in url:
            platform = "instagram"
        else:
            platform = "instagram" # fallback as requested
            
    if output:
        # User specified custom output directory
        target_dir = output
    else:
        # Use default directory based on platform
        target_dir = get_platform_dir(platform)
        
    console.print(f"[bold cyan]Platform:[/bold cyan] [green]{platform}[/green]")
    console.print(f"[bold cyan]Saving to:[/bold cyan] [green]{target_dir}[/green]")
    
    if cookies_browser:
        # Check if we have a cached cookie file
        cache_path = get_cookie_cache_path(cookies_browser)
        if not cache_path.exists():
            console.print(f"[bold yellow]First time extracting {cookies_browser} cookies...[/bold yellow]")
            console.print("[dim]Note: If this hangs, please ensure Chrome is completely closed to unlock the database.[/dim]")
            try:
                # Use yt-dlp to extract cookies to our cache file
                # This only happens once
                subprocess.run([
                    "yt-dlp", 
                    "--cookies-from-browser", cookies_browser, 
                    "--cookies", str(cache_path), 
                    "--skip-download", "https://www.youtube.com"
                ], capture_output=True, check=True)
                console.print(f"[green]Cookies cached to {cache_path}[/green]")
            except Exception as e:
                console.print(f"[bold red]Failed to extract cookies from {cookies_browser}: {e}[/bold red]")
                cookies_browser = None # fallback to no cookies
        
        # Use the cached file for the actual download
        if cache_path.exists():
            cookies = cache_path
            cookies_browser = None # Disable browser extraction in downloader.py as we have the file

    result_path = download_video(
        url=url,
        platform=platform,
        output_dir=target_dir,
        quality=quality,
        download_thumbnail=not no_thumb,
        download_transcript=not no_transcript,
        cookies_browser=cookies_browser,
        cookies_file=cookies
    )
    
    if result_path:
        console.print(f"\n[bold green]✓ Successfully saved video bundle to: {result_path}[/bold green]")
    else:
        console.print("\n[bold red]x Failed to download video bundle.[/bold red]")
        raise typer.Exit(code=1)

@app.command("edit")
def edit(
    video_id: str = typer.Argument(..., help="Video ID or path to edit"),
    preset: str = typer.Option("base", "-p", "--preset", help="Editing preset to apply")
):
    """
    Edit a video using predefined presets (trim, caption, watermark, bgm).
    """
    console.print(f"[yellow]Edit command is under development. Preset: {preset}[/yellow]")

@app.command("ai")
def ai():
    """
    AI enhancement tools (crop, highlights, dub, thumbnail).
    """
    console.print("[yellow]AI commands are under development.[/yellow]")

@app.command()
def edit(
    video_path: Path = typer.Argument(..., help="Path to the video file to edit"),
    text: Optional[str] = typer.Option(None, "--text", help="Text to add as watermark"),
    image: Optional[Path] = typer.Option(None, "--image", help="Image to add as watermark"),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Path for the output video"),
    position: str = typer.Option("bottom_right", "--position", help="Position for the watermark")
):
    """
    Apply edits to a video (watermarking, etc.).
    """
    if not video_path.exists():
        console.print(f"[bold red]File not found: {video_path}[/bold red]")
        raise typer.Exit(1)

    if output is None:
        # Create a default output filename: name_edited.mp4
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

@app.command("config")
def config():
    """
    Manage configuration and API keys.
    """
    console.print("[yellow]Config command is under development.[/yellow]")

@app.command("batch")
def batch():
    """
    Process multiple URLs from a text file.
    """
    console.print("[yellow]Batch command is under development.[/yellow]")

if __name__ == "__main__":
    app()
