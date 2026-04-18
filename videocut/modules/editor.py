import subprocess
import os
from pathlib import Path
from videocut.modules.downloader import check_ffmpeg
from rich.console import Console

console = Console()

def add_text_watermark(input_path: Path, output_path: Path, text: str, position: str = "bottom_right"):
    """
    Adds a text watermark to the video using FFmpeg.
    Position can be: top_left, top_right, bottom_left, bottom_right, center.
    """
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        console.print("[bold red]FFmpeg not found. Cannot process video.[/bold red]")
        return False

    # Map position to drawtext coordinates
    pos_map = {
        "top_left": "x=10:y=10",
        "top_right": "x=w-tw-10:y=10",
        "bottom_left": "x=10:y=h-th-10",
        "bottom_right": "x=w-tw-10:y=h-th-10",
        "center": "x=(w-tw)/2:y=(h-th)/2"
    }
    pos_cmd = pos_map.get(position, pos_map["bottom_right"])

    # Drawtext filter
    # Note: Using :fontcolor=white:fontsize=24:shadowcolor=black@0.5:shadowx=2:shadowy=2
    vf_filter = f"drawtext=text='{text}':{pos_cmd}:fontcolor=white:fontsize=36:shadowcolor=black@0.6:shadowx=2:shadowy=2"

    cmd = [
        str(ffmpeg_path),
        "-i", str(input_path),
        "-vf", vf_filter,
        "-codec:a", "copy", # Copy audio without re-encoding
        "-preset", "fast",
        str(output_path),
        "-y" # Overwrite output
    ]

    console.print(f"[blue]Adding text watermark: '{text}'...[/blue]")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        console.print("[green]Watermark added successfully![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]FFmpeg failed: {e.stderr.decode()}[/bold red]")
        return False

def add_image_watermark(input_path: Path, output_path: Path, watermark_path: Path, position: str = "bottom_right"):
    """
    Adds an image overlay/watermark to the video.
    """
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        return False

    # Map position for overlay
    pos_map = {
        "top_left": "10:10",
        "top_right": "main_w-overlay_w-10:10",
        "bottom_left": "10:main_h-overlay_h-10",
        "bottom_right": "main_w-overlay_w-10:main_h-overlay_h-10",
        "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
    }
    pos_cmd = pos_map.get(position, "main_w-overlay_w-10:main_h-overlay_h-10")

    cmd = [
        str(ffmpeg_path),
        "-i", str(input_path),
        "-i", str(watermark_path),
        "-filter_complex", f"overlay={pos_cmd}",
        "-codec:a", "copy",
        "-preset", "fast",
        str(output_path),
        "-y"
    ]

    console.print(f"[blue]Adding image watermark...[/blue]")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
